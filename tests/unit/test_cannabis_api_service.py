"""
Service tests for CannabisApiService.
Coverage: Run pytest ... --cov-fail-under=80 to enforce >80%.
"""
import pytest
from unittest.mock import patch, MagicMock, Mock
import time
import requests

from app.services.cannabis_api_service import CannabisApiService, RateLimiter, TTLCache

@pytest.fixture
def service():
    """Fixture for CannabisApiService."""
    return CannabisApiService()

def test_fetch_cultivar_by_name_success(service, caplog):
    """Test successful cultivar fetch by name."""
    with patch('requests.Session.get') as mock_get:
        mock_get.return_value.json.return_value = {'strains': [{'id': '123', 'name': 'Blue Dream', 'type': 'hybrid'}]}
        mock_get.return_value.status_code = 200
        result = service.fetch_cultivar_by_name('Blue Dream')
        assert result is not None
        assert 'Blue Dream' in result['name']

# RateLimiter Tests
def test_rate_limiter_init():
    """Test RateLimiter initialization."""
    limiter = RateLimiter(max_requests=10, time_window=60)
    assert limiter.max_requests == 10
    assert limiter.time_window == 60
    assert len(limiter.requests) == 0

def test_rate_limiter_allows_requests_under_limit():
    """Test that requests under the limit are allowed immediately."""
    limiter = RateLimiter(max_requests=5, time_window=60)
    for i in range(5):
        start_time = time.time()
        limiter.wait_if_needed()
        end_time = time.time()
        assert end_time - start_time < 0.01
        assert len(limiter.requests) == i + 1

def test_rate_limiter_enforces_rate_limit():
    """Test that rate limiting is enforced when at the limit."""
    limiter = RateLimiter(max_requests=2, time_window=2)
    now = time.time()
    limiter.requests = [now - 0.5, now - 0.4]
    
    start_time = time.time()
    limiter.wait_if_needed()
    end_time = time.time()
    
    assert end_time - start_time > 0.1
    assert 1 <= len(limiter.requests) <= 3

def test_rate_limiter_cleans_old_requests():
    """Test that old requests are cleaned from the window."""
    limiter = RateLimiter(max_requests=2, time_window=1)
    limiter.requests = [time.time() - 2.0]
    
    start_time = time.time()
    limiter.wait_if_needed()
    end_time = time.time()
    
    assert end_time - start_time < 0.01

# TTLCache Tests
def test_ttl_cache_init():
    """Test TTLCache initialization."""
    cache = TTLCache(ttl_seconds=3600, max_size=100)
    assert cache.ttl_seconds == 3600
    assert cache.max_size == 100
    assert len(cache._cache) == 0

def test_ttl_cache_set_and_get():
    """Test setting and getting values from the cache."""
    cache = TTLCache(ttl_seconds=3600, max_size=10)
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"
    assert cache.get("key2") is None

def test_ttl_cache_expiration():
    """Test TTL expiration."""
    cache = TTLCache(ttl_seconds=1, max_size=10)
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"
    time.sleep(1.1)
    assert cache.get("key1") is None

def test_ttl_cache_max_size_eviction():
    """Test max size eviction."""
    cache = TTLCache(ttl_seconds=3600, max_size=2)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")
    assert cache.get("key1") is None
    assert cache.get("key2") == "value2"
    assert cache.get("key3") == "value3"

def test_ttl_cache_clear():
    """Test clearing the cache."""
    cache = TTLCache(ttl_seconds=3600, max_size=10)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.clear()
    assert len(cache._cache) == 0
    assert cache.get("key1") is None

# CannabisApiService Tests
def test_service_init(service):
    """Test service initialization."""
    assert service.session is not None
    assert service.rate_limiter is not None
    assert service.cache is not None
    assert service.BASE_URL == "https://the-cannabis-api.vercel.app/api"

@patch('app.config.config.Config.CANNABIS_API_KEY', 'test-api-key')
def test_service_init_with_api_key():
    """Test service initialization with an API key."""
    service = CannabisApiService()
    assert service.api_key == 'test-api-key'
    assert service.session.headers.get('Authorization') == 'Bearer test-api-key'

def test_make_request_success(service):
    """Test a successful HTTP request."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "test"}
    
    with patch.object(service.session, 'get', return_value=mock_response):
        result = service._make_request("strains")
    
    assert result == {"data": "test"}

def test_make_request_retry_on_500_error(service):
    """Test retry logic on server error."""
    mock_response_500 = Mock()
    mock_response_500.status_code = 500
    
    mock_response_200 = Mock()
    mock_response_200.status_code = 200
    mock_response_200.json.return_value = {"data": "success"}
    
    with patch.object(service.session, 'get', side_effect=[mock_response_500, mock_response_200]):
        with patch('time.sleep'):
            result = service._make_request("strains", retries=1)
    
    assert result == {"data": "success"}

def test_make_request_no_retry_on_400_error(service):
    """Test no retry on client error."""
    mock_response_400 = Mock()
    mock_response_400.status_code = 400
    mock_response_400.text = "Bad Request"
    
    with patch.object(service.session, 'get', return_value=mock_response_400):
        result = service._make_request("strains")
    
    assert result is None

def test_make_request_timeout_retry(service):
    """Test retry on timeout."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "success"}
    
    with patch.object(service.session, 'get', side_effect=[requests.exceptions.Timeout(), mock_response]):
        with patch('time.sleep'):
            result = service._make_request("strains", retries=1)
    
    assert result == {"data": "success"}

def test_map_api_data_to_cultivar(service):
    """Test API data to cultivar mapping."""
    api_data = {
        "id": "123", "name": "Test Item", "race": "sativa", "thc": 20.5,
        "cbd": 1.2, "description": "Test description"
    }
    result = service._map_api_data_to_cultivar(api_data, "123")
    
    assert result['external_id'] == 'cannabis_api'
    assert result['external_id_value'] == '123'
    assert result['name'] == 'Test Item'
    assert result['sativa'] == 80
    assert result['indica'] == 20
    assert result['thc_content'] == 20.5

def test_get_cache_key(service):
    """Test cache key generation."""
    key1 = service._get_cache_key("fetch_by_name", name="test")
    key2 = service._get_cache_key("fetch_by_name", name="test")
    key3 = service._get_cache_key("search_by_type", type="sativa")
    
    assert key1 == key2
    assert key1 != key3

def test_fetch_cultivar_by_name_not_found(service):
    """Test item fetch when not found."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": []}
    
    with patch.object(service.session, 'get', return_value=mock_response):
        result = service.fetch_cultivar_by_name("Nonexistent Item")
    
    assert result is None

def test_search_cultivars_by_type_success(service):
    """Test successful item search by type."""
    items_data = [{"id": "1", "name": "Sativa 1", "race": "sativa"}]
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": items_data}
    
    with patch.object(service.session, 'get', return_value=mock_response):
        result = service.search_cultivars_by_type("sativa")
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]['name'] == 'Sativa 1'

def test_caching_behavior(service):
    """Test that caching is working."""
    api_data = {"id": "1", "name": "Cached Item", "race": "hybrid"}
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [api_data]}
    
    with patch.object(service.session, 'get', return_value=mock_response) as mock_get:
        result1 = service.fetch_cultivar_by_name("Cached Item")
        result2 = service.fetch_cultivar_by_name("Cached Item")
        
        mock_get.assert_called_once()
        assert result1 == result2

def test_validation_skips_invalid_data(service, caplog):
    """Test that validation skips items with invalid data."""
    mock_data = {"name": "Invalid", "indica": 150, "id": "123"}
    
    with patch.object(service, '_make_request', return_value={"data": [mock_data]}):
        result = service.fetch_cultivar_by_name("Invalid")
        assert result is None
        assert "Validation failed" in caplog.text

@patch('app.services.cannabis_api_service.sync_create_breeder')
def test_breeder_integration(mock_create_breeder, service):
    """Test breeder integration."""
    api_data = {"id": "123", "name": "Test Item", "race": "hybrid", "breeder_name": "Test Breeder"}
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [api_data]}
    
    mock_create_breeder.return_value = {"success": True, "breeder_id": 1}
    
    with patch.object(service.session, 'get', return_value=mock_response):
        result = service.fetch_cultivar_by_name("Test Item")
        
        assert result is not None
        mock_create_breeder.assert_called_once_with({'name': 'Test Breeder', 'user_id': 1}, session=None, user_id=None)
        assert result['breeder_id'] == 1

def test_no_strain_leaks(service):
    """Test that no 'strain' terminology leaks in the output."""
    api_data = {"id": "123", "name": "Test Item", "race": "hybrid"}
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [api_data]}
    
    with patch.object(service.session, 'get', return_value=mock_response):
        result = service.fetch_cultivar_by_name("Test Item")
        
        assert result is not None
        
        def check_keys(d):
            for k, v in d.items():
                assert "strain" not in k.lower()
                if isinstance(v, dict):
                    check_keys(v)
        
        check_keys(result)

def test_clear_cache(service):
    """Test clearing the cache."""
    service.cache.set("key1", "value1")
    assert service.cache.get("key1") == "value1"
    service.clear_cache()
    assert service.cache.get("key1") is None

def test_get_cache_stats(service):
    """Test getting cache statistics."""
    service.cache.set("key1", "value1")
    service.cache.set("key2", "value2")
    stats = service.get_cache_stats()
    assert stats['total_entries'] == 2
    assert stats['max_size'] == 1000
    assert stats['ttl_seconds'] == 3600

@patch('app.services.cannabis_api_service.sync_create_breeder')
def test_breeder_injection(mock_create_breeder, service):
    """Test breeder integration with an injected user ID."""
    api_data = {"id": "123", "name": "Test Item", "race": "hybrid", "breeder_name": "Test Breeder"}
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [api_data]}
    
    mock_create_breeder.return_value = {"success": True, "breeder_id": 2}
    
    with patch.object(service.session, 'get', return_value=mock_response):
        result = service.fetch_cultivar_by_name("Test Item", user_id=999)
        
        assert result is not None
        assert result['breeder_id'] == 2

if __name__ == "__main__":
    pytest.main(["-v", __file__, "--cov=app/services", "--cov-report=term-missing"])