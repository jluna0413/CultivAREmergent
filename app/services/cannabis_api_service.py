"""
The_Cannabis_API service for strain/cultivar data retrieval.

This module provides a service class for interacting with The_Cannabis_API,
including HTTP client with retry logic, rate limiting, caching, and
strain-to-cultivar mapping.
"""

import time
import threading
from typing import Optional, List, Dict, Any

import requests

from app.config.config import Config
from app.logger import logger
from app.utils.cannabis_api_mapper import map_cannabis_api_strain


class RateLimiter:
    """Thread-safe rate limiter for HTTP requests."""
    
    def __init__(self, max_requests: int, time_window: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Maximum number of requests allowed
            time_window: Time window in seconds (default: 60 for requests per minute)
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
        self._lock = threading.Lock()
    
    def wait_if_needed(self) -> None:
        """Wait if rate limit would be exceeded."""
        with self._lock:
            now = time.time()
            
            # Remove requests outside the time window
            self.requests = [req_time for req_time in self.requests if now - req_time < self.time_window]
            
            # If at limit, wait
            if len(self.requests) >= self.max_requests:
                sleep_time = self.time_window - (now - self.requests[0]) + 0.1
                if sleep_time > 0:
                    logger.info(f"Rate limit reached, sleeping for {sleep_time:.2f} seconds")
                    time.sleep(sleep_time)
                    # Clean up old requests after sleep
                    now = time.time()
                    self.requests = [req_time for req_time in self.requests if now - req_time < self.time_window]
            
            # Add current request
            self.requests.append(now)


class TTLCache:
    """Simple TTL cache implementation using standard library."""
    
    def __init__(self, ttl_seconds: int = 3600, max_size: int = 1000):
        """
        Initialize TTL cache.
        
        Args:
            ttl_seconds: Time to live in seconds (default: 3600 = 1 hour)
            max_size: Maximum number of entries (default: 1000)
        """
        self.ttl_seconds = ttl_seconds
        self.max_size = max_size
        self._cache = {}
        self._timestamps = {}
        self._lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        with self._lock:
            if key in self._cache:
                timestamp = self._timestamps.get(key, 0)
                if time.time() - timestamp < self.ttl_seconds:
                    return self._cache[key]
                else:
                    # Expired, remove
                    del self._cache[key]
                    del self._timestamps[key]
            return None
    
    def set(self, key: str, value: Any) -> None:
        """Set value in cache with current timestamp."""
        with self._lock:
            # If at max size, remove oldest entry
            if len(self._cache) >= self.max_size:
                oldest_key = min(self._timestamps.keys(), key=lambda k: self._timestamps[k])
                del self._cache[oldest_key]
                del self._timestamps[oldest_key]
            
            self._cache[key] = value
            self._timestamps[key] = time.time()
    
    def clear(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()
            self._timestamps.clear()


class CannabisApiService:
    """Service for interacting with The_Cannabis_API."""
    
    BASE_URL = "https://the-cannabis-api.vercel.app/api"
    
    def __init__(self):
        """Initialize the service with configuration."""
        self.api_key = Config.CANNABIS_API_KEY
        self.rate_limiter = RateLimiter(max_requests=100, time_window=60)  # 100 requests per minute
        self.cache = TTLCache(ttl_seconds=3600)  # 1 hour TTL
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'User-Agent': 'CultivAR/1.0',
            'Accept': 'application/json',
        })
        
        # Add API key if available
        if self.api_key:
            self.session.headers['Authorization'] = f'Bearer {self.api_key}'
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, str]] = None, retries: int = 3) -> Optional[Dict[str, Any]]:
        """
        Make HTTP request with retry logic and exponential backoff.
        
        Args:
            endpoint: API endpoint path (without base URL)
            params: Query parameters
            retries: Number of retry attempts
            
        Returns:
            Response JSON or None if failed
        """
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        
        for attempt in range(retries + 1):
            try:
                # Apply rate limiting
                self.rate_limiter.wait_if_needed()
                
                logger.debug(f"Making request to {url} (attempt {attempt + 1})")
                
                response = self.session.get(url, params=params, timeout=30)
                
                # Check for HTTP errors
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:
                    # Rate limited, wait longer
                    wait_time = min(2 ** attempt, 30)
                    logger.warning(f"Rate limited, waiting {wait_time} seconds before retry {attempt + 1}")
                    time.sleep(wait_time)
                    continue
                elif 500 <= response.status_code < 600:
                    # Server error, retry with exponential backoff
                    if attempt < retries:
                        wait_time = 0.5 * (2 ** attempt)
                        logger.warning(f"Server error {response.status_code}, retrying in {wait_time}s (attempt {attempt + 1})")
                        time.sleep(wait_time)
                        continue
                else:
                    # Client error, don't retry
                    logger.error(f"HTTP error {response.status_code}: {response.text}")
                    return None
                    
            except requests.exceptions.Timeout:
                logger.warning(f"Request timeout on attempt {attempt + 1}")
                if attempt < retries:
                    wait_time = 0.5 * (2 ** attempt)
                    logger.info(f"Retrying in {wait_time}s")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error("All retry attempts failed due to timeout")
                    return None
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Request error on attempt {attempt + 1}: {e}")
                if attempt < retries:
                    wait_time = 0.5 * (2 ** attempt)
                    logger.info(f"Retrying in {wait_time}s")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error("All retry attempts failed due to request error")
                    return None
                    
            except Exception as e:
                logger.error(f"Unexpected error on attempt {attempt + 1}: {e}")
                if attempt < retries:
                    wait_time = 0.5 * (2 ** attempt)
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error("All retry attempts failed due to unexpected error")
                    return None
        
        logger.error(f"All {retries + 1} attempts failed for {url}")
        return None
    
    def _map_strain_to_cultivar(self, strain_data: Dict[str, Any], provider_id: str) -> Dict[str, Any]:
        """
        Transform strain data to cultivar format with external ID tracking.
        
        Args:
            strain_data: Raw strain data from The_Cannabis_API
            provider_id: Original provider's ID for external_id_value
            
        Returns:
            Cultivar-formatted dictionary
        """
        # Maps API 'strain' data to internal 'cultivar' format
        # Convert strain data using the mapper (handles name, race, effects, etc.)
        cultivar_data = map_cannabis_api_strain(strain_data)
        
        # Track the external data source and original provider ID
        # Maps to external_id='cannabis_api', external_id_value=provider_id
        cultivar_data['external_id'] = 'cannabis_api'
        cultivar_data['external_id_value'] = provider_id
        
        return cultivar_data
    
    def _get_cache_key(self, method: str, **kwargs) -> str:
        """Generate cache key for request parameters."""
        # Sort kwargs to ensure consistent key generation
        sorted_items = sorted(kwargs.items())
        params_str = '&'.join(f"{k}={v}" for k, v in sorted_items if v is not None)
        return f"{method}:{params_str}"
    
    def fetch_strain_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Fetch strain by name from The_Cannabis_API and return as cultivar.
        
        Args:
            name: Strain name to search for
            
        Returns:
            Single cultivar-formatted dictionary or None if not found
        """
        if not name or not name.strip():
            logger.warning("Empty strain name provided")
            return None
        
        # Check cache first
        cache_key = self._get_cache_key("fetch_by_name", name=name.strip())
        cached_result = self.cache.get(cache_key)
        if cached_result is not None:
            logger.debug(f"Cache hit for strain name: {name}")
            return cached_result
        
        # Make API request
        params = {'name': name.strip()}
        response_data = self._make_request("strains", params=params)
        
        if not response_data:
            logger.error(f"Failed to fetch strain data for name: {name}")
            return None
        
        # Handle different response formats
        strains = []
        if isinstance(response_data, dict):
            if 'data' in response_data:
                strains = response_data['data']
            elif 'strains' in response_data:
                strains = response_data['strains']
            else:
                strains = [response_data]
        elif isinstance(response_data, list):
            strains = response_data
        else:
            logger.error(f"Unexpected response format for strain name: {name}")
            return None
        
        # Find exact name match or first result
        strain = None
        for s in strains:
            if s.get('name', '').lower() == name.lower():
                strain = s
                break
        
        if not strain and strains:
            strain = strains[0]
        
        if not strain:
            logger.info(f"No strain found for name: {name}")
            return None
        
        # Transform to cultivar format
        provider_id = str(strain.get('id', ''))
        if not provider_id:
            logger.warning(f"No ID found for strain: {name}")
            return None
        
        cultivar = self._map_strain_to_cultivar(strain, provider_id)
        
        # Cache the result
        self.cache.set(cache_key, cultivar)
        
        logger.info(f"Successfully fetched and mapped strain: {name}")
        return cultivar
    
    def search_strains_by_type(self, strain_type: str) -> List[Dict[str, Any]]:
        """
        Search strains by type and return as list of cultivars.
        
        Args:
            strain_type: Type of strain (e.g., 'sativa', 'indica', 'hybrid')
            
        Returns:
            List of cultivar-formatted dictionaries
        """
        if not strain_type or not strain_type.strip():
            logger.warning("Empty strain type provided")
            return []
        
        # Check cache first
        cache_key = self._get_cache_key("search_by_type", type=strain_type.strip())
        cached_result = self.cache.get(cache_key)
        if cached_result is not None:
            logger.debug(f"Cache hit for strain type: {strain_type}")
            return cached_result
        
        # Make API request
        params = {'type': strain_type.strip()}
        response_data = self._make_request("strains", params=params)
        
        if not response_data:
            logger.error(f"Failed to fetch strain data for type: {strain_type}")
            return []
        
        # Extract strains from response
        strains = []
        if isinstance(response_data, dict):
            if 'data' in response_data:
                strains = response_data['data']
            elif 'strains' in response_data:
                strains = response_data['strains']
            else:
                strains = [response_data]
        elif isinstance(response_data, list):
            strains = response_data
        else:
            logger.error(f"Unexpected response format for strain type: {strain_type}")
            return []
        
        # Transform to cultivar format
        cultivars = []
        for strain in strains:
            provider_id = str(strain.get('id', ''))
            if not provider_id:
                logger.warning(f"No ID found for strain, skipping: {strain.get('name', 'unknown')}")
                continue
            
            cultivar = self._map_strain_to_cultivar(strain, provider_id)
            cultivars.append(cultivar)
        
        # Cache the result
        self.cache.set(cache_key, cultivars)
        
        logger.info(f"Successfully fetched {len(cultivars)} strains for type: {strain_type}")
        return cultivars
    
    def get_strains_by_effect(self, effect: str) -> List[Dict[str, Any]]:
        """
        Get strains by effect and return as list of cultivars.
        
        Args:
            effect: Effect to search for (e.g., 'relaxed', 'happy', 'euphoric')
            
        Returns:
            List of cultivar-formatted dictionaries
        """
        if not effect or not effect.strip():
            logger.warning("Empty effect provided")
            return []
        
        # Check cache first
        cache_key = self._get_cache_key("search_by_effect", effect=effect.strip())
        cached_result = self.cache.get(cache_key)
        if cached_result is not None:
            logger.debug(f"Cache hit for effect: {effect}")
            return cached_result
        
        # Make API request
        params = {'effect': effect.strip()}
        response_data = self._make_request("strains", params=params)
        
        if not response_data:
            logger.error(f"Failed to fetch strain data for effect: {effect}")
            return []
        
        # Extract strains from response
        strains = []
        if isinstance(response_data, dict):
            if 'data' in response_data:
                strains = response_data['data']
            elif 'strains' in response_data:
                strains = response_data['strains']
            else:
                strains = [response_data]
        elif isinstance(response_data, list):
            strains = response_data
        else:
            logger.error(f"Unexpected response format for effect: {effect}")
            return []
        
        # Transform to cultivar format
        cultivars = []
        for strain in strains:
            provider_id = str(strain.get('id', ''))
            if not provider_id:
                logger.warning(f"No ID found for strain, skipping: {strain.get('name', 'unknown')}")
                continue
            
            cultivar = self._map_strain_to_cultivar(strain, provider_id)
            cultivars.append(cultivar)
        
        # Cache the result
        self.cache.set(cache_key, cultivars)
        
        logger.info(f"Successfully fetched {len(cultivars)} strains for effect: {effect}")
        return cultivars
    
    def clear_cache(self) -> None:
        """Clear the internal cache."""
        self.cache.clear()
        logger.info("Cache cleared")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self.cache._lock:
            return {
                'total_entries': len(self.cache._cache),
                'max_size': self.cache.max_size,
                'ttl_seconds': self.cache.ttl_seconds
            }