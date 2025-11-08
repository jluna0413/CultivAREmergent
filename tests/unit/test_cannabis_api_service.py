"""
Unit tests for CannabisApiService.

Tests cover HTTP client functionality, retry logic, rate limiting,
TTL caching, strain-to-cultivar mapping, and public API methods.
"""

import time
import unittest
from unittest.mock import Mock, patch, MagicMock
import requests

import pytest

from app.services.cannabis_api_service import (
    CannabisApiService, 
    RateLimiter, 
    TTLCache
)
from app.utils.cannabis_api_mapper import map_cannabis_api_strain


class TestRateLimiter(unittest.TestCase):
    """Test the RateLimiter class."""
    
    def test_init(self):
        """Test rate limiter initialization."""
        limiter = RateLimiter(max_requests=10, time_window=60)
        self.assertEqual(limiter.max_requests, 10)
        self.assertEqual(limiter.time_window, 60)
        self.assertEqual(len(limiter.requests), 0)
    
    def test_wait_if_needed_allows_requests_under_limit(self):
        """Test that requests under the limit are allowed immediately."""
        limiter = RateLimiter(max_requests=5, time_window=60)
        
        # Should allow requests up to the limit
        for i in range(5):
            start_time = time.time()
            limiter.wait_if_needed()
            end_time = time.time()
            
            # Should not have waited (less than 1ms)
            self.assertLess(end_time - start_time, 0.01)
            self.assertEqual(len(limiter.requests), i + 1)
    
    def test_wait_if_needed_enforces_rate_limit(self):
        """Test that rate limiting is enforced when at limit."""
        limiter = RateLimiter(max_requests=2, time_window=2)  # Longer window to avoid cleanup
        
        # Add two requests right away
        now = time.time()
        limiter.requests = [now - 0.5, now - 0.4]  # Recent requests within window
        
        # Third request should wait
        start_time = time.time()
        limiter.wait_if_needed()
        end_time = time.time()
        
        # Should have waited at least some time
        self.assertGreater(end_time - start_time, 0.1)
        # After waiting, we should have the new request plus remaining old requests
        # (old requests are cleaned up if they're now outside the time window)
        self.assertGreaterEqual(len(limiter.requests), 1)  # At least the new request
        self.assertLessEqual(len(limiter.requests), 3)   # But no more than 3 total
    
    def test_wait_if_needed_cleans_old_requests(self):
        """Test that old requests are cleaned from the window."""
        limiter = RateLimiter(max_requests=2, time_window=1)
        
        # Add old request
        limiter.requests = [time.time() - 2.0]  # Outside the 1-second window
        
        # Should not enforce limit since old request is cleaned
        start_time = time.time()
        limiter.wait_if_needed()
        end_time = time.time()
        
        # Should not have waited significantly
        self.assertLess(end_time - start_time, 0.01)


class TestTTLCache(unittest.TestCase):
    """Test the TTLCache class."""
    
    def test_init(self):
        """Test cache initialization."""
        cache = TTLCache(ttl_seconds=3600, max_size=100)
        self.assertEqual(cache.ttl_seconds, 3600)
        self.assertEqual(cache.max_size, 100)
        self.assertEqual(len(cache._cache), 0)
    
    def test_set_and_get(self):
        """Test setting and getting values."""
        cache = TTLCache(ttl_seconds=3600, max_size=10)
        
        cache.set("key1", "value1")
        self.assertEqual(cache.get("key1"), "value1")
        
        # Non-existent key
        self.assertIsNone(cache.get("key2"))
    
    def test_ttl_expiration(self):
        """Test TTL expiration."""
        cache = TTLCache(ttl_seconds=1, max_size=10)  # 1 second TTL
        
        cache.set("key1", "value1")
        self.assertEqual(cache.get("key1"), "value1")
        
        # Wait for expiration
        time.sleep(1.1)
        self.assertIsNone(cache.get("key1"))
    
    def test_max_size_eviction(self):
        """Test max size eviction."""
        cache = TTLCache(ttl_seconds=3600, max_size=2)
        
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")  # Should evict oldest
        
        # Oldest key should be evicted
        self.assertIsNone(cache.get("key1"))
        self.assertEqual(cache.get("key2"), "value2")
        self.assertEqual(cache.get("key3"), "value3")
    
    def test_clear(self):
        """Test cache clearing."""
        cache = TTLCache(ttl_seconds=3600, max_size=10)
        
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        
        cache.clear()
        
        self.assertEqual(len(cache._cache), 0)
        self.assertIsNone(cache.get("key1"))
        self.assertIsNone(cache.get("key2"))


class TestCannabisApiService(unittest.TestCase):
    """Test the CannabisApiService class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.service = CannabisApiService()
    
    def test_init(self):
        """Test service initialization."""
        self.assertIsNotNone(self.service.session)
        self.assertIsNotNone(self.service.rate_limiter)
        self.assertIsNotNone(self.service.cache)
        self.assertEqual(self.service.BASE_URL, "https://the-cannabis-api.vercel.app/api")
    
    @patch('app.config.config.Config.CANNABIS_API_KEY', 'test-api-key')
    def test_init_with_api_key(self):
        """Test service initialization with API key."""
        service = CannabisApiService()
        self.assertEqual(service.api_key, 'test-api-key')
        self.assertEqual(service.session.headers.get('Authorization'), 'Bearer test-api-key')
    
    def test_make_request_success(self):
        """Test successful HTTP request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        
        with patch.object(self.service.session, 'get', return_value=mock_response):
            result = self.service._make_request("strains")
        
        self.assertEqual(result, {"data": "test"})
    
    def test_make_request_retry_on_500_error(self):
        """Test retry logic on server error."""
        mock_response_500 = Mock()
        mock_response_500.status_code = 500
        mock_response_500.json.return_value = {"error": "server error"}
        
        mock_response_200 = Mock()
        mock_response_200.status_code = 200
        mock_response_200.json.return_value = {"data": "success"}
        
        with patch.object(self.service.session, 'get', side_effect=[mock_response_500, mock_response_200]):
            with patch('time.sleep'):  # Mock sleep to speed up test
                result = self.service._make_request("strains", retries=1)
        
        self.assertEqual(result, {"data": "success"})
    
    def test_make_request_no_retry_on_400_error(self):
        """Test no retry on client error."""
        mock_response_400 = Mock()
        mock_response_400.status_code = 400
        mock_response_400.text = "Bad Request"
        
        with patch.object(self.service.session, 'get', return_value=mock_response_400):
            result = self.service._make_request("strains")
        
        self.assertIsNone(result)
    
    def test_make_request_timeout_retry(self):
        """Test retry on timeout."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "success"}
        
        with patch.object(self.service.session, 'get', side_effect=[
            requests.exceptions.Timeout(),
            mock_response
        ]):
            with patch('time.sleep'):  # Mock sleep to speed up test
                result = self.service._make_request("strains", retries=1)
        
        self.assertEqual(result, {"data": "success"})
    
    def test_map_strain_to_cultivar(self):
        """Test strain to cultivar mapping."""
        strain_data = {
            "id": "123",
            "name": "Test Strain",
            "race": "sativa",
            "thc": 20.5,
            "cbd": 1.2,
            "description": "Test description"
        }
        
        result = self.service._map_strain_to_cultivar(strain_data, "123")
        
        # Check that external ID tracking is added
        self.assertEqual(result['external_id'], 'cannabis_api')
        self.assertEqual(result['external_id_value'], '123')
        
        # Check that mapper functionality is preserved
        self.assertEqual(result['name'], 'Test Strain')
        self.assertEqual(result['sativa'], 100)
        self.assertEqual(result['indica'], 0)
        self.assertEqual(result['thc_content'], 20.5)
        self.assertEqual(result['cbd_content'], 1.2)
        self.assertEqual(result['description'], 'Test description')
    
    def test_get_cache_key(self):
        """Test cache key generation."""
        key1 = self.service._get_cache_key("fetch_by_name", name="test")
        key2 = self.service._get_cache_key("fetch_by_name", name="test")
        key3 = self.service._get_cache_key("search_by_type", type="sativa")
        
        # Same parameters should produce same key
        self.assertEqual(key1, key2)
        
        # Different parameters should produce different keys
        self.assertNotEqual(key1, key3)
    
    def test_fetch_strain_by_name_success(self):
        """Test successful strain fetch by name."""
        strain_data = {
            "id": "123",
            "name": "Test Strain",
            "race": "hybrid",
            "thc": 15.0
        }
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [strain_data]}
        
        with patch.object(self.service.session, 'get', return_value=mock_response):
            result = self.service.fetch_strain_by_name("Test Strain")
        
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'Test Strain')
        self.assertEqual(result['external_id'], 'cannabis_api')
        self.assertEqual(result['external_id_value'], '123')
    
    def test_fetch_strain_by_name_not_found(self):
        """Test strain fetch when not found."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        
        with patch.object(self.service.session, 'get', return_value=mock_response):
            result = self.service.fetch_strain_by_name("Nonexistent Strain")
        
        self.assertIsNone(result)
    
    def test_fetch_strain_by_name_empty_name(self):
        """Test strain fetch with empty name."""
        result = self.service.fetch_strain_by_name("")
        self.assertIsNone(result)
        
        result = self.service.fetch_strain_by_name("   ")
        self.assertIsNone(result)
    
    def test_search_strains_by_type_success(self):
        """Test successful strain search by type."""
        strains_data = [
            {"id": "1", "name": "Sativa 1", "race": "sativa"},
            {"id": "2", "name": "Sativa 2", "race": "sativa"}
        ]
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": strains_data}
        
        with patch.object(self.service.session, 'get', return_value=mock_response):
            result = self.service.search_strains_by_type("sativa")
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        
        # Check first result
        self.assertEqual(result[0]['name'], 'Sativa 1')
        self.assertEqual(result[0]['external_id'], 'cannabis_api')
        self.assertEqual(result[0]['external_id_value'], '1')
    
    def test_search_strains_by_type_empty_response(self):
        """Test strain search with empty response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        
        with patch.object(self.service.session, 'get', return_value=mock_response):
            result = self.service.search_strains_by_type("sativa")
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
    
    def test_get_strains_by_effect_success(self):
        """Test successful strain search by effect."""
        strains_data = [
            {"id": "1", "name": "Happy Strain", "effects": ["happy", "euphoric"]},
            {"id": "2", "name": "Relaxed Strain", "effects": ["relaxed", "happy"]}
        ]
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": strains_data}
        
        with patch.object(self.service.session, 'get', return_value=mock_response):
            result = self.service.get_strains_by_effect("happy")
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'Happy Strain')
        self.assertEqual(result[1]['name'], 'Relaxed Strain')
    
    def test_get_strains_by_effect_no_strains(self):
        """Test effect search with no matching strains."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        
        with patch.object(self.service.session, 'get', return_value=mock_response):
            result = self.service.get_strains_by_effect("nonexistent")
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
    
    def test_caching_behavior(self):
        """Test that caching is working."""
        strain_data = {"id": "1", "name": "Cached Strain", "race": "hybrid"}
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [strain_data]}
        
        with patch.object(self.service.session, 'get', return_value=mock_response) as mock_get:
            # First call should hit the API
            result1 = self.service.fetch_strain_by_name("Cached Strain")
            
            # Second call should use cache
            result2 = self.service.fetch_strain_by_name("Cached Strain")
            
            # Should have called API only once
            self.assertEqual(mock_get.call_count, 1)
            
            # Results should be identical
            self.assertEqual(result1, result2)
    
    def test_cache_expiration(self):
        """Test that cache expires after TTL."""
        strain_data = {"id": "1", "name": "Expiring Strain", "race": "indica"}
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [strain_data]}
        
        with patch.object(self.service.session, 'get', return_value=mock_response) as mock_get:
            # First call
            result1 = self.service.fetch_strain_by_name("Expiring Strain")
            
            # Clear cache to force expiration
            self.service.cache.clear()
            
            # Second call should hit API again
            result2 = self.service.fetch_strain_by_name("Expiring Strain")
            
            # Should have called API twice
            self.assertEqual(mock_get.call_count, 2)
    
    def test_clear_cache(self):
        """Test cache clearing."""
        # Add something to cache
        self.service.cache.set("test", "value")
        
        # Clear cache
        self.service.clear_cache()
        
        # Should be empty
        self.assertIsNone(self.service.cache.get("test"))
    
    def test_get_cache_stats(self):
        """Test cache statistics."""
        self.service.cache.set("key1", "value1")
        self.service.cache.set("key2", "value2")
        
        stats = self.service.get_cache_stats()
        
        self.assertEqual(stats['total_entries'], 2)
        self.assertEqual(stats['max_size'], 1000)
        self.assertEqual(stats['ttl_seconds'], 3600)
    
    def test_api_error_handling(self):
        """Test API error handling."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        
        with patch.object(self.service.session, 'get', return_value=mock_response):
            result = self.service.fetch_strain_by_name("Test")
        
        self.assertIsNone(result)
    
    def test_network_error_handling(self):
        """Test network error handling."""
        with patch.object(self.service.session, 'get', side_effect=requests.exceptions.ConnectionError()):
            result = self.service.fetch_strain_by_name("Test")
        
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()