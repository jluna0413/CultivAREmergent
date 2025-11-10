"""
Run: pytest -v --cov=app/services --cov-report=term-missing --cov-fail-under=80 (baseline from .coverage)
"""
import pytest
from unittest.mock import patch, Mock
import time
import requests

from app.services.cannabis_api_service import CannabisApiService, RateLimiter, TTLCache

@pytest.fixture
def service():
    """Fixture for CannabisApiService."""
    return CannabisApiService()

def test_no_strain_leaks(service):
    """Test that no 'strain' terminology leaks in the output."""
    with patch('requests.Session.get') as mock_get:
        mock_get.return_value.json.return_value = {'data': [{'id': '123', 'name': 'Test Item', 'race': 'hybrid'}]}
        mock_get.return_value.status_code = 200
        result = service.fetch_cultivar_by_name("Test Item")
        
        assert result is not None
        
        def check_keys(d):
            for k, v in d.items():
                assert "strain" not in k.lower()
                if isinstance(v, dict):
                    check_keys(v)
        
        check_keys(result)

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
    with patch('requests.Session.get') as mock_get:
        mock_get.return_value.json.return_value = {'data': []}
        mock_get.return_value.status_code = 200
        result = service.fetch_cultivar_by_name("Nonexistent Item")
        assert result is None

def test_search_cultivars_by_type_success(service):
    """Test successful item search by type."""
    with patch('requests.Session.get') as mock_get:
        mock_get.return_value.json.return_value = {'data': [{'id': '1', 'name': 'Sativa 1', 'race': 'sativa'}]}
        mock_get.return_value.status_code = 200
        result = service.search_cultivars_by_type("sativa")
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]['name'] == 'Sativa 1'

def test_search_cultivars_by_type_empty_response(service):
    """Test item search with empty response."""
    with patch('requests.Session.get') as mock_get:
        mock_get.return_value.json.return_value = {'data': []}
        mock_get.return_value.status_code = 200
        result = service.search_cultivars_by_type("sativa")
        assert isinstance(result, list)
        assert len(result) == 0

def test_caching_behavior(service):
    """Test that caching is working."""
    with patch('requests.Session.get') as mock_get:
        mock_get.return_value.json.return_value = {'data': [{'id': '1', 'name': 'Cached Item', 'race': 'hybrid'}]}
        mock_get.return_value.status_code = 200
        result1 = service.fetch_cultivar_by_name("Cached Item")
        result2 = service.fetch_cultivar_by_name("Cached Item")
        mock_get.assert_called_once()
        assert result1 == result2

def test_validation_skips_invalid_data(service, caplog):
    """Test that validation skips items with invalid data."""
    with patch('requests.Session.get') as mock_get:
        mock_get.return_value.json.return_value = {'data': [{'id': '123', 'name': 'Invalid', 'indica': 150}]}
        mock_get.return_value.status_code = 200
        result = service.fetch_cultivar_by_name("Invalid")
        assert result is None
        assert "Validation failed" in caplog.text

@patch('app.services.cannabis_api_service.sync_create_breeder')
def test_breeder_integration(mock_create_breeder, service):
    """Test breeder integration."""
    with patch('requests.Session.get') as mock_get:
        mock_get.return_value.json.return_value = {'data': [{'id': '123', 'name': 'Test Item', 'race': 'hybrid', 'breeder_name': 'Test Breeder'}]}
        mock_get.return_value.status_code = 200
        mock_create_breeder.return_value = {"success": True, "breeder_id": 1}
        result = service.fetch_cultivar_by_name("Test Item")
        assert result is not None
        mock_create_breeder.assert_called_once_with({'name': 'Test Breeder', 'user_id': 1}, None)
        assert result['breeder_id'] == 1

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
    with patch('requests.Session.get') as mock_get:
        mock_get.return_value.json.return_value = {'data': [{'id': '123', 'name': 'Test', 'race': 'hybrid', 'breeder_name': 'Test Breeder'}]}
        mock_get.return_value.status_code = 200
        mock_create_breeder.return_value = {'success': True, 'breeder_id': 2}
        result = service.fetch_cultivar_by_name('Test', user_id=999)
        assert 'breeder_id' in result

def test_get_cultivars_by_effect(service):
    """Test getting cultivars by effect."""
    with patch('requests.Session.get') as mock_get:
        mock_get.return_value.json.return_value = {'data': [{'id': '1', 'name': 'Happy', 'effects': ['happy']}]}
        mock_get.return_value.status_code = 200
        result = service.get_cultivars_by_effect('happy')
        assert len(result) == 1
        assert result[0]['name'] == 'Happy'


    def test_make_request_retry_on_multiple_500s(service):
        """_make_request should retry multiple times on 5xx and eventually succeed."""
        mock_resp_500 = type("R", (), {})()
        mock_resp_500.status_code = 500

        mock_resp_200 = type("R", (), {})()
        mock_resp_200.status_code = 200
        mock_resp_200.json = lambda: {"data": "ok-500s"}

        with patch.object(service.session, 'get', side_effect=[mock_resp_500, mock_resp_500, mock_resp_200]):
            with patch('time.sleep'):
                result = service._make_request("strains", retries=2)

        assert result == {"data": "ok-500s"}


    def test_make_request_timeout_then_success(service):
        """_make_request should handle Timeout and succeed on retry."""
        mock_resp_200 = type("R", (), {})()
        mock_resp_200.status_code = 200
        mock_resp_200.json = lambda: {"data": "ok-timeout"}

        with patch.object(service.session, 'get', side_effect=[requests.exceptions.Timeout(), mock_resp_200]):
            with patch('time.sleep'):
                result = service._make_request("strains", retries=1)

        assert result == {"data": "ok-timeout"}


    def test_fetch_cultivar_by_name_handles_strains_key(service):
        """When response contains 'strains' key, it should be extracted as items."""
        response = {'strains': [{'id': '222', 'name': 'Strain Key', 'race': 'sativa'}]}
        with patch('requests.Session.get') as mock_get:
            mock_get.return_value.json.return_value = response
            mock_get.return_value.status_code = 200
            result = service.fetch_cultivar_by_name('Strain Key')

        assert result is not None
        assert result['name'] == 'Strain Key'


    def test_fetch_cultivar_by_name_single_dict_response(service):
        """A single dict response (no 'data'/'strains') should be handled as one item."""
        single = {'id': '333', 'name': 'Single Item', 'race': 'indica'}
        with patch('requests.Session.get') as mock_get:
            mock_get.return_value.json.return_value = single
            mock_get.return_value.status_code = 200
            result = service.fetch_cultivar_by_name('Single Item')

        assert result is not None
        assert result['name'] == 'Single Item'


    def test_fetch_cultivar_by_name_missing_provider_id_returns_none(service):
        """If provider id missing from API item, function returns None."""
        with patch('requests.Session.get') as mock_get:
            mock_get.return_value.json.return_value = {'data': [{'name': 'No ID', 'race': 'hybrid'}]}
            mock_get.return_value.status_code = 200
            result = service.fetch_cultivar_by_name('No ID')

        assert result is None


    def test_make_request_handles_429_then_success(service):
        """_make_request should wait on 429 and succeed afterwards."""
        resp429 = type("R", (), {})()
        resp429.status_code = 429

        resp200 = type("R", (), {})()
        resp200.status_code = 200
        resp200.json = lambda: {"data": "ok-429"}

        with patch.object(service.session, 'get', side_effect=[resp429, resp200]):
            with patch('time.sleep'):
                result = service._make_request('strains', retries=1)

        assert result == {"data": "ok-429"}


    def test_empty_name_and_empty_search_and_effect(service):
        """Empty inputs for fetch/search/effect should return None or empty list."""
        assert service.fetch_cultivar_by_name('') is None
        assert service.search_cultivars_by_type('') == []
        assert service.get_cultivars_by_effect('') == []


    def test_search_cultivars_by_type_handles_strains_key(service):
        resp = {'strains': [{'id': '900', 'name': 'TypeStrain', 'race': 'sativa'}]}
        with patch('requests.Session.get') as mock_get:
            mock_get.return_value.json.return_value = resp
            mock_get.return_value.status_code = 200
            result = service.search_cultivars_by_type('sativa')

        assert isinstance(result, list)
        assert result[0]['name'] == 'TypeStrain'


    def test_get_cultivars_by_effect_handles_strains_key(service):
        resp = {'strains': [{'id': '910', 'name': 'EffectStrain', 'effects': ['happy']} ]}
        with patch('requests.Session.get') as mock_get:
            mock_get.return_value.json.return_value = resp
            mock_get.return_value.status_code = 200
            result = service.get_cultivars_by_effect('happy')

        assert isinstance(result, list)
        assert result[0]['name'] == 'EffectStrain'


    def test_make_request_429_forced_branch(service):
        """Ensure the 429 branch executes by forcing a 429 then 200 response and no-oping rate limiter."""
        resp429 = type("R", (), {})()
        resp429.status_code = 429

        resp200 = type("R", (), {})()
        resp200.status_code = 200
        resp200.json = lambda: {"data": "ok-429-forced"}

        # No-op the rate limiter to remove timing influence
        service.rate_limiter.wait_if_needed = lambda: None

        with patch.object(service.session, 'get', side_effect=[resp429, resp200]):
            with patch('time.sleep'):
                result = service._make_request('strains', retries=1)

        assert result == {"data": "ok-429-forced"}


    def test_search_cultivars_by_type_skips_item_without_id(service):
        """Items missing 'id' should be skipped in search_cultivars_by_type."""
        resp = {'data': [{'name': 'NoID', 'race': 'sativa'}, {'id': '1000', 'name': 'Good', 'race': 'sativa'}]}
        with patch('requests.Session.get') as mock_get:
            mock_get.return_value.json.return_value = resp
            mock_get.return_value.status_code = 200
            result = service.search_cultivars_by_type('sativa')

        assert isinstance(result, list)
        assert any(r['name'] == 'Good' for r in result)


    def test_make_request_handles_429_and_retries(service):
        """_make_request should retry on 429 and eventually return success."""
        mock_resp_429 = type("R", (), {})()
        mock_resp_429.status_code = 429

        mock_resp_200 = type("R", (), {})()
        mock_resp_200.status_code = 200
        mock_resp_200.json = lambda: {"data": "ok"}

        with patch.object(service.session, 'get', side_effect=[mock_resp_429, mock_resp_200]):
            with patch('time.sleep'):
                result = service._make_request("strains")

        assert result == {"data": "ok"}


    def test_make_request_handles_request_exception(service):
        """_make_request should return None after repeated RequestException."""
        with patch.object(service.session, 'get', side_effect=requests.exceptions.RequestException()):
            with patch('time.sleep'):
                result = service._make_request("strains", retries=1)

        assert result is None


    def test_fetch_cultivar_by_name_without_breeder(service):
        """If breeder_name is absent, no breeder creation should be attempted."""
        with patch('requests.Session.get') as mock_get:
            mock_get.return_value.json.return_value = {'data': [{'id': '123', 'name': 'No Breeder', 'race': 'hybrid'}]}
            mock_get.return_value.status_code = 200
            with patch('app.services.cannabis_api_service.sync_create_breeder') as mock_create:
                result = service.fetch_cultivar_by_name("No Breeder")
                # ensure sync_create_breeder was not called because breeder_name missing
                mock_create.assert_not_called()
                assert result is not None