import logging
import re
import json
from typing import Any, Dict, Optional, List
from datetime import datetime

from pydantic import BaseModel, Field
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy

logger = logging.getLogger(__name__)

# Schema for LLM Extraction
class CannabisStrainSchema(BaseModel):
    name: str = Field(..., description="Name of the strain/cultivar")
    breeder_name: str = Field(..., description="Name of the breeder")
    description: str = Field("", description="Detailed description of the strain, effects, and lineage")
    type: str = Field("Hybrid", description="Type: Indica, Sativa, or Hybrid")
    indica_pct: Optional[float] = Field(None, description="Indica percentage (0-100)")
    sativa_pct: Optional[float] = Field(None, description="Sativa percentage (0-100)")
    ruderalis_pct: Optional[float] = Field(None, description="Ruderalis percentage (0-100)")
    genetics_type: Optional[str] = Field(None, description="e.g. Indica-Dominant")
    
    
    # Lineage
    lineage: Dict[str, str] = Field(default_factory=dict, description="Parents: parent1, parent2")
    
    # Cannabinoids
    thc_pct: Optional[str] = Field(None, description="THC % or range")
    cbd_pct: Optional[str] = Field(None, description="CBD % or range")
    cbg_pct: Optional[str] = Field(None, description="CBG %")
    thcv_pct: Optional[str] = Field(None, description="THCV %")
    cbc_pct: Optional[str] = Field(None, description="CBC %")
    cbn_pct: Optional[str] = Field(None, description="CBN %")
    
    # Terpenes
    terpene_profile: Dict[str, float] = Field(default_factory=dict, description="Terpenes: myrcene, limonene, caryophyllene, etc.")
    
    # Sensory
    flavors: List[str] = Field(default_factory=list, description="List of flavors")
    aromas: List[str] = Field(default_factory=list, description="List of aromas")
    effects: List[str] = Field(default_factory=list, description="List of effects")
    medical_benefits: List[str] = Field(default_factory=list, description="List of medical benefits")
    negative_effects: List[str] = Field(default_factory=list, description="List of negative effects")
    
    # Growing
    flowering_type: Optional[str] = Field(None, description="Autoflower or Photoperiod")
    flowering_time_min: Optional[int] = Field(None, description="Min flowering days")
    flowering_time_max: Optional[int] = Field(None, description="Max flowering days")
    yield_indoor: Optional[str] = Field(None, description="Indoor yield description")
    yield_outdoor: Optional[str] = Field(None, description="Outdoor yield description")
    height_indoor: Optional[str] = Field(None, description="Indoor height")
    grow_difficulty: Optional[str] = Field(None, description="Grow difficulty (Easy, Moderate, Difficult)")
    
    image_urls: List[str] = Field(default_factory=list, description="URLs of strain images")

class BreederSchema(BaseModel):
    name: str = Field(..., description="Name of the breeder")
    description: Optional[str] = Field(None, description="Description or history of the breeder")
    country: Optional[str] = Field(None, description="Country of origin")
    website: Optional[str] = Field(None, description="Official website URL")
    logo_url: Optional[str] = Field(None, description="URL of the breeder's logo")

class SeedFinderScraper:
    """
    SeedFinder.eu scraper using Crawl4AI and Ollama (Hybrid Approach).
    
    Authentication:
    - Uses local Ollama instance (provider: ollama/functiongemma:270m) for intelligent extraction.
    """
    
    BASE_URL = "https://en.seedfinder.eu"
    
    def __init__(self):
        self.browser_config = BrowserConfig(
            headless=True,
            viewport_width=1920,
            viewport_height=1080,
            verbose=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # Initialize LLM Strategy with Ollama
        self.llm_config = LLMConfig(provider="ollama/granite4:micro-h", api_token="no-token")

        # Initialize LLM Strategy with Ollama
        self.strain_strategy = LLMExtractionStrategy(
            llm_config=self.llm_config,
            schema=CannabisStrainSchema.model_json_schema(),
            extraction_type="schema",
            instruction=(
                "Extract detailed cannabis strain information. "
                "Include: Breeder, Genetics (Indica/Sativa/Ruderalis %), "
                "Lineage (Parent strains), "
                "Cannabinoids (THC, CBD, CBG, etc.), "
                "Terpenes (Myrcene, Limonene, etc with %), "
                "Effects, Medical Benefits, Flavors, Aromas. "
                "Growing info: Flowering time (min/max days), Yields, Height, Difficulty. "
                "Extract Image URLs if possible."
            ),
            input_format="markdown",
            verbose=True
        )
        
        # Initialize LLM Strategy for Breeders
        self.breeder_strategy = LLMExtractionStrategy(
            llm_config=self.llm_config,
            schema=BreederSchema.model_json_schema(),
            extraction_type="schema",
            instruction=(
                "Extract breeder information from the page. "
                "Focus on: Breeder Name, Description/History, Country of Origin, "
                "Official Website, and Logo URL."
            ),
            input_format="markdown",
            verbose=True
        )

    async def search_strain(self, strain_name: str) -> Optional[Dict[str, Any]]:
        """
        Search for a strain and extract details using Crawl4AI + Ollama.
        Uses the database index instead of search for reliability.
        """
        # Normalize strain name for URL construction
        # SeedFinder uses underscores and lowercase for URLs
        normalized = strain_name.replace(' ', '_').replace('-', '_')
        first_letter = normalized[0].lower() if normalized else 'a'
        
        # Try the database alphabetical index (more reliable than search)
        # Format: /database/strains/alphabetical/{letter}/
        index_url = f"{self.BASE_URL}/database/strains/alphabetical/{first_letter}/"
        
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            logger.info(f"Browsing strain index for {strain_name} at {index_url}")
            result = await crawler.arun(url=index_url, cache_mode=CacheMode.BYPASS)
            
            if not result.success:
                logger.error(f"Index crawl failed: {result.error_message}")
                return None
            
            # Find strain link in the index page
            strain_url = None
            search_content = (result.html or "") + (result.markdown or "")
            
            # Get all strain-info links
            all_links = re.findall(r'(/strain-info/[a-zA-Z0-9_\-/]+)', search_content)
            logger.info(f"Found {len(all_links)} total strain-info links")
            
            # Normalize the search term for matching
            strain_lower = strain_name.lower().replace(' ', '-').replace('_', '-')
            strain_underscore = strain_name.lower().replace(' ', '_').replace('-', '_')
            
            # Search through all links for a match
            for link in all_links:
                link_lower = link.lower()
                if strain_lower in link_lower or strain_underscore in link_lower:
                    strain_url = f"{self.BASE_URL}{link}" if link.startswith('/') else link
                    break
            
            if not strain_url:
                logger.warning(f"No valid strain link found for {strain_name}")
                return None
            
            logger.info(f"Found strain page: {strain_url}")
            
            # 2. Extraction Phase (with Ollama)
            extract_config = CrawlerRunConfig(
                extraction_strategy=self.strain_strategy,
                cache_mode=CacheMode.BYPASS
            )
            
            detail_result = await crawler.arun(url=strain_url, config=extract_config)
            
            if detail_result.success:
                logger.info(f"Extraction completed. Content length: {len(detail_result.extracted_content or '')}")
                
                data = None
                if detail_result.extracted_content:
                    try:
                        # Parse LLM JSON output
                        parsed = json.loads(detail_result.extracted_content)
                        
                        # Crawl4AI might return a list of items
                        if isinstance(parsed, list):
                            data = parsed[0] if parsed else None
                        else:
                            data = parsed if parsed else None
                        
                        if data:
                            # Add metadata
                            data['source'] = 'seedfinder'
                            data['source_url'] = strain_url
                            data['seedfinder_id'] = strain_url.split('/')[-2] if len(strain_url.split('/')) > 2 else None
                            
                            logger.info(f"Successfully extracted strain data: {data.get('name', 'Unknown')}")
                            return data
                            
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to decode LLM JSON: {e}")
                        logger.debug(f"Raw content: {detail_result.extracted_content}")
                
                # Fallback: return basic info extracted from URL if LLM returned nothing useful
                logger.warning("LLM extraction returned empty or no data. Returning basic info from URL.")
                parts = strain_url.rstrip('/').split('/')
                if len(parts) >= 2:
                    strain_slug = parts[-2]  # e.g., "auto-blue-dream"
                    breeder_slug = parts[-1]  # e.g., "dutch-headshop"
                    
                    return {
                        'name': strain_slug.replace('-', ' ').replace('_', ' ').title(),
                        'breeder_name': breeder_slug.replace('-', ' ').replace('_', ' ').title(),
                        'source': 'seedfinder',
                        'source_url': strain_url,
                        'seedfinder_id': strain_slug,
                        'extraction_note': 'Basic extraction from URL (LLM extraction returned empty)'
                    }
            else:
                logger.error(f"Extraction failed: {detail_result.error_message}")
                
            return None

    async def search_breeder(self, breeder_name: str) -> Optional[Dict[str, Any]]:
        """
        Search for a breeder and extract details using Crawl4AI + Ollama.
        Uses the database index instead of search for reliability.
        """
        # Normalize breeder name for matching
        first_letter = breeder_name[0].lower() if breeder_name else 'a'
        
        # Try the database breeder index
        # Format: /database/breeder/ (all breeders page)
        index_url = f"{self.BASE_URL}/database/breeder/"
        
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            logger.info(f"Browsing breeder index for {breeder_name} at {index_url}")
            result = await crawler.arun(url=index_url, cache_mode=CacheMode.BYPASS)
            
            if not result.success:
                logger.error(f"Breeder index crawl failed: {result.error_message}")
                return None
            
            # Find breeder link in the index page
            breeder_url = None
            search_content = (result.html or "") + (result.markdown or "")
            
            # Get all breeder links
            all_links = re.findall(r'(/database/breeder/[a-zA-Z0-9_\-]+)', search_content)
            logger.info(f"Found {len(all_links)} total breeder links")
            
            # Normalize the search term for matching
            breeder_lower = breeder_name.lower().replace(' ', '-').replace('_', '-').replace("'", "")
            breeder_underscore = breeder_name.lower().replace(' ', '_').replace('-', '_').replace("'", "")
            
            # Search through all links for a match
            for link in all_links:
                link_lower = link.lower()
                if breeder_lower in link_lower or breeder_underscore in link_lower:
                    breeder_url = f"{self.BASE_URL}{link}" if link.startswith('/') else link
                    break
            
            if not breeder_url:
                logger.warning(f"No valid breeder link found for {breeder_name}")
                return None
                
            logger.info(f"Found breeder page: {breeder_url}")
            
            # 2. Extraction Phase
            extract_config = CrawlerRunConfig(
                extraction_strategy=self.breeder_strategy,
                cache_mode=CacheMode.ENABLED
            )
            
            detail_result = await crawler.arun(url=breeder_url, config=extract_config)
            
            if detail_result.success:
                data = None
                if detail_result.extracted_content:
                    try:
                        parsed = json.loads(detail_result.extracted_content)
                        if isinstance(parsed, list):
                            data = parsed[0] if parsed else None
                        else:
                            data = parsed if parsed else None
                        
                        if data:
                            data['source'] = 'seedfinder'
                            data['source_url'] = breeder_url
                            data['source_id'] = breeder_url.strip('/').split('/')[-1]
                            logger.info(f"Successfully extracted breeder data: {data.get('name', 'Unknown')}")
                            return data
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to decode Breeder LLM JSON: {e}")
                
                # Fallback: return basic info from URL
                logger.warning("Breeder LLM extraction returned empty. Returning basic info from URL.")
                breeder_slug = breeder_url.strip('/').split('/')[-1]
                return {
                    'name': breeder_slug.replace('-', ' ').replace('_', ' ').title(),
                    'source': 'seedfinder',
                    'source_url': breeder_url,
                    'source_id': breeder_slug,
                    'extraction_note': 'Basic extraction from URL (LLM extraction returned empty)'
                }
            else:
                logger.error(f"Breeder extraction failed: {detail_result.error_message}")
                 
            return None

    async def get_all_breeders(self) -> List[Dict[str, str]]:
        """
        Fetch all breeders from the SeedFinder database index.
        Returns a list of dicts with 'name', 'slug', and 'url' for each breeder.
        """
        index_url = f"{self.BASE_URL}/database/breeder/"
        breeders = []
        
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            logger.info(f"Fetching all breeders from {index_url}")
            result = await crawler.arun(url=index_url, cache_mode=CacheMode.BYPASS)
            
            if not result.success:
                logger.error(f"Failed to fetch breeder index: {result.error_message}")
                return []
            
            # Extract breeder links from content
            search_content = (result.html or "") + (result.markdown or "")
            
            # Pattern: /database/breeder/slug-name
            links = re.findall(r'/database/breeder/([a-zA-Z0-9_\-]+)', search_content)
            
            # Deduplicate
            seen = set()
            for slug in links:
                if slug not in seen and slug not in ['', 'search']:
                    seen.add(slug)
                    breeders.append({
                        'slug': slug,
                        'name': slug.replace('-', ' ').replace('_', ' ').title(),
                        'url': f"{self.BASE_URL}/database/breeder/{slug}"
                    })
            
            logger.info(f"Found {len(breeders)} unique breeders")
            
        return breeders

    async def get_breeder_strains(self, breeder_slug: str) -> List[Dict[str, str]]:
        """
        Fetch all strains for a specific breeder.
        Returns a list of dicts with 'name', 'slug', and 'url' for each strain.
        """
        breeder_url = f"{self.BASE_URL}/database/breeder/{breeder_slug}"
        strains = []
        
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            logger.info(f"Fetching strains for breeder {breeder_slug}")
            result = await crawler.arun(url=breeder_url, cache_mode=CacheMode.BYPASS)
            
            if not result.success:
                logger.error(f"Failed to fetch breeder page: {result.error_message}")
                return []
            
            # Extract strain-info links from content
            search_content = (result.html or "") + (result.markdown or "")
            
            # Pattern: /strain-info/strain-slug/breeder-slug
            pattern = rf'/strain-info/([a-zA-Z0-9_\-]+)/{re.escape(breeder_slug)}'
            links = re.findall(pattern, search_content, re.IGNORECASE)
            
            # Deduplicate
            seen = set()
            for slug in links:
                if slug not in seen:
                    seen.add(slug)
                    strains.append({
                        'slug': slug,
                        'breeder_slug': breeder_slug,
                        'name': slug.replace('-', ' ').replace('_', ' ').title(),
                        'url': f"{self.BASE_URL}/strain-info/{slug}/{breeder_slug}"
                    })
            
            logger.info(f"Found {len(strains)} strains for breeder {breeder_slug}")
            
        return strains

    async def extract_strain_from_url(self, strain_url: str) -> Optional[Dict[str, Any]]:
        """
        Extract detailed strain info from a known strain URL.
        Uses LLM extraction with granite4:micro-h.
        """
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            extract_config = CrawlerRunConfig(
                extraction_strategy=self.strain_strategy,
                cache_mode=CacheMode.BYPASS
            )
            
            logger.info(f"Extracting strain data from {strain_url}")
            result = await crawler.arun(url=strain_url, config=extract_config)
            
            if result.success:
                data = None
                if result.extracted_content:
                    try:
                        parsed = json.loads(result.extracted_content)
                        if isinstance(parsed, list):
                            data = parsed[0] if parsed else None
                        else:
                            data = parsed if parsed else None
                        
                        if data:
                            data['source'] = 'seedfinder'
                            data['source_url'] = strain_url
                            # Extract IDs from URL
                            parts = strain_url.rstrip('/').split('/')
                            if len(parts) >= 2:
                                data['seedfinder_id'] = parts[-2]
                                data['breeder_slug'] = parts[-1]
                            return data
                    except json.JSONDecodeError as e:
                        logger.error(f"JSON decode error: {e}")
                
                # Fallback to URL-based extraction
                parts = strain_url.rstrip('/').split('/')
                if len(parts) >= 2:
                    return {
                        'name': parts[-2].replace('-', ' ').replace('_', ' ').title(),
                        'breeder_slug': parts[-1],
                        'source': 'seedfinder',
                        'source_url': strain_url,
                        'seedfinder_id': parts[-2],
                        'extraction_note': 'Fallback extraction from URL'
                    }
            
            return None

    def _fuzzy_match(self, query: str, candidate: str) -> bool:
        """Simple fuzzy string matching."""
        query_clean = query.lower().strip()
        candidate_clean = candidate.lower().strip()
        if query_clean == candidate_clean:
            return True
        if query_clean in candidate_clean or candidate_clean in query_clean:
            return True
        return False
    
    async def close(self):
        """No-op for Crawl4AI (context manager handles it)."""
        pass
