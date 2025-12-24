"""
Breeder Spotlight Agent

Highlights top breeders, showcases their work, and provides breeder analytics.

Part of Discovery Agents.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum
import logging

from pydantic import BaseModel, Field

from ..base import (
    AgentRole,
    AgentContext,
    AgentResult,
    BaseAgent,
    AgentRegistry,
)
from ...gamification import gamification_engine

logger = logging.getLogger(__name__)


class BreederTier(str, Enum):
    """Breeder reputation tiers"""
    LEGENDARY = "legendary"
    ELITE = "elite"
    ESTABLISHED = "established"
    RISING = "rising"
    NEWCOMER = "newcomer"


class BreederProfile(BaseModel):
    """Breeder profile data"""
    id: int
    name: str
    tier: BreederTier
    years_active: int
    total_strains: int
    signature_strains: List[str]
    specialties: List[str]
    awards: List[str]
    average_rating: float = Field(ge=0, le=5)
    verified: bool = False
    nft_holder: bool = False


class BreederAnalytics(BaseModel):
    """Breeder performance analytics"""
    popularity_rank: int
    trending_score: float
    community_rating: float
    strain_success_rate: float
    recent_releases: int


class BreederSpotlightAgent(BaseAgent):
    """
    Breeder discovery and spotlight agent.
    
    Capabilities:
    - Weekly breeder spotlights
    - Breeder analytics and rankings
    - New release alerts
    - Breeder verification status
    - NFT-holder breeder highlights
    
    Integrates with:
    - Breeder database
    - NFT verification (Algorand)
    - Gamification (XP for discoveries)
    """
    
    def __init__(self):
        super().__init__(
            agent_id="breeder_spotlight",
            name="Breeder Spotlight",
            role=AgentRole.DISCOVERY,
            description="Breeder discovery, spotlights, and analytics",
        )
        
        # Register MCP tools
        self.register_tool(
            "get_spotlight",
            self.get_weekly_spotlight,
            "Get this week's featured breeder"
        )
        self.register_tool(
            "get_breeder_profile",
            self.get_breeder_profile,
            "Get detailed breeder profile"
        )
        self.register_tool(
            "get_top_breeders",
            self.get_top_breeders,
            "Get top ranked breeders"
        )
        self.register_tool(
            "get_trending_breeders",
            self.get_trending_breeders,
            "Get currently trending breeders"
        )
        self.register_tool(
            "search_breeders",
            self.search_breeders,
            "Search breeders by criteria"
        )
        
        # Mock breeder database
        self._breeder_db = self._load_mock_breeders()
        
    async def execute(self, context: AgentContext, **kwargs) -> AgentResult:
        """Execute breeder spotlight"""
        action = kwargs.get("action", "spotlight")
        
        try:
            if action == "spotlight":
                result = await self.get_weekly_spotlight()
            elif action == "profile":
                result = await self.get_breeder_profile(
                    breeder_id=kwargs.get("breeder_id")
                )
            elif action == "top":
                result = await self.get_top_breeders(
                    limit=kwargs.get("limit", 10),
                    category=kwargs.get("category", "overall"),
                )
            elif action == "trending":
                result = await self.get_trending_breeders(
                    limit=kwargs.get("limit", 5)
                )
            elif action == "search":
                result = await self.search_breeders(
                    query=kwargs.get("query", ""),
                    specialty=kwargs.get("specialty"),
                )
            else:
                result = {"error": f"Unknown action: {action}"}
                
            # Award XP
            if context.user_id:
                gamification_engine.award_xp(
                    context.user_id, 5, "breeder_discovery"
                )
                
            return AgentResult(
                success=True,
                agent_id=self.agent_id,
                output=result,
                confidence=0.9,
                xp_reward=5,
                next_actions=["view_strains", "follow_breeder", "compare_breeders"],
            )
            
        except Exception as e:
            logger.error(f"BreederSpotlight error: {e}")
            return AgentResult(
                success=False,
                agent_id=self.agent_id,
                output=None,
                error=str(e),
            )
    
    async def get_weekly_spotlight(self) -> Dict[str, Any]:
        """Get this week's featured breeder"""
        # In production, would rotate weekly
        featured = self._breeder_db[0]  # Mock: first breeder
        
        return {
            "spotlight_type": "weekly",
            "week_of": datetime.utcnow().strftime("%Y-%m-%d"),
            "featured_breeder": {
                **featured,
                "spotlight_reason": "Consistent quality and community engagement",
                "featured_strain": featured["signature_strains"][0] if featured["signature_strains"] else None,
            },
            "previous_spotlights": [
                {"name": "Mephisto Genetics", "week": "2024-12-01"},
                {"name": "In House Genetics", "week": "2024-11-24"},
            ],
            "next_spotlight_preview": "Coming soon: A legendary breeder with 30+ years experience",
        }
    
    async def get_breeder_profile(self, breeder_id: Optional[int] = None) -> Dict[str, Any]:
        """Get detailed breeder profile"""
        if breeder_id is None:
            return {"error": "breeder_id required"}
            
        breeder = next((b for b in self._breeder_db if b["id"] == breeder_id), None)
        
        if not breeder:
            return {"error": f"Breeder {breeder_id} not found"}
            
        # Enhanced profile with analytics
        return {
            "profile": breeder,
            "analytics": {
                "popularity_rank": self._get_popularity_rank(breeder_id),
                "trending_score": 0.85,
                "community_rating": breeder["average_rating"],
                "strain_count": breeder["total_strains"],
                "verified": breeder["verified"],
            },
            "recent_activity": [
                {"type": "new_release", "strain": "New Cross #1", "date": "2024-12-01"},
                {"type": "award", "award": "Best Hybrid 2024", "date": "2024-11-15"},
            ],
            "popular_strains": breeder["signature_strains"][:5],
            "similar_breeders": self._get_similar_breeders(breeder_id),
        }
    
    async def get_top_breeders(
        self, 
        limit: int = 10, 
        category: str = "overall"
    ) -> Dict[str, Any]:
        """Get top ranked breeders"""
        sorted_breeders = sorted(
            self._breeder_db,
            key=lambda b: b["average_rating"],
            reverse=True
        )
        
        # Filter by category if specified
        if category == "indica":
            sorted_breeders = [b for b in sorted_breeders if "indica" in b.get("specialties", [])]
        elif category == "sativa":
            sorted_breeders = [b for b in sorted_breeders if "sativa" in b.get("specialties", [])]
        elif category == "autoflower":
            sorted_breeders = [b for b in sorted_breeders if "autoflower" in b.get("specialties", [])]
            
        top = sorted_breeders[:limit]
        
        return {
            "category": category,
            "total_breeders": len(self._breeder_db),
            "top_breeders": [
                {
                    "rank": i + 1,
                    **breeder,
                }
                for i, breeder in enumerate(top)
            ],
            "categories": ["overall", "indica", "sativa", "autoflower", "cbd"],
        }
    
    async def get_trending_breeders(self, limit: int = 5) -> Dict[str, Any]:
        """Get currently trending breeders"""
        # Mock trending data
        trending = [
            {"breeder": self._breeder_db[0], "trend_reason": "New strain release", "trend_score": 0.95},
            {"breeder": self._breeder_db[1], "trend_reason": "Award winner", "trend_score": 0.88},
        ]
        
        return {
            "period": "This Week",
            "trending": trending[:limit],
            "rising_stars": [
                {"name": "New Breeder Co", "reason": "Viral TikTok"},
            ],
        }
    
    async def search_breeders(
        self, 
        query: str = "", 
        specialty: Optional[str] = None
    ) -> Dict[str, Any]:
        """Search breeders by criteria"""
        results = []
        
        for breeder in self._breeder_db:
            score = 0
            
            # Name match
            if query.lower() in breeder["name"].lower():
                score += 0.5
                
            # Specialty match
            if specialty and specialty in breeder.get("specialties", []):
                score += 0.3
                
            # Always include with base score
            if not query or score > 0:
                results.append({
                    **breeder,
                    "match_score": round(score if score > 0 else 0.1, 2),
                })
                
        results.sort(key=lambda x: x["match_score"], reverse=True)
        
        return {
            "query": query,
            "specialty_filter": specialty,
            "results": results[:20],
            "total_found": len(results),
        }
    
    def _load_mock_breeders(self) -> List[Dict]:
        """Load mock breeder database"""
        return [
            {
                "id": 1,
                "name": "Mephisto Genetics",
                "tier": BreederTier.LEGENDARY.value,
                "years_active": 12,
                "total_strains": 50,
                "signature_strains": ["Sour Stomper", "Double Grape", "Mango Smile"],
                "specialties": ["autoflower", "high-thc"],
                "awards": ["Best Autoflower 2023", "Spannabis Winner"],
                "average_rating": 4.9,
                "verified": True,
                "nft_holder": True,
            },
            {
                "id": 2,
                "name": "Barney's Farm",
                "tier": BreederTier.LEGENDARY.value,
                "years_active": 30,
                "total_strains": 100,
                "signature_strains": ["LSD", "Critical Kush", "Gorilla Zkittlez"],
                "specialties": ["indica", "hybrid", "award-winning"],
                "awards": ["High Times Cup x10", "Spannabis Winner"],
                "average_rating": 4.7,
                "verified": True,
                "nft_holder": False,
            },
            {
                "id": 3,
                "name": "Night Owl Seeds",
                "tier": BreederTier.ELITE.value,
                "years_active": 5,
                "total_strains": 25,
                "signature_strains": ["Owl Pellets", "Blue Microverse", "Spotless Mind"],
                "specialties": ["autoflower", "exotic-terps"],
                "awards": ["Community Favorite 2024"],
                "average_rating": 4.8,
                "verified": True,
                "nft_holder": True,
            },
            {
                "id": 4,
                "name": "Ethos Genetics",
                "tier": BreederTier.ELITE.value,
                "years_active": 8,
                "total_strains": 40,
                "signature_strains": ["Mandarin Cookies", "Cherry Gar See Ya", "Planet of the Grapes"],
                "specialties": ["photoperiod", "high-thc", "exotic"],
                "awards": ["Emerald Cup Winner"],
                "average_rating": 4.6,
                "verified": True,
                "nft_holder": False,
            },
        ]
    
    def _get_popularity_rank(self, breeder_id: int) -> int:
        """Get breeder's popularity rank"""
        sorted_ids = [b["id"] for b in sorted(self._breeder_db, key=lambda x: x["average_rating"], reverse=True)]
        return sorted_ids.index(breeder_id) + 1 if breeder_id in sorted_ids else 999
    
    def _get_similar_breeders(self, breeder_id: int) -> List[Dict]:
        """Get similar breeders"""
        target = next((b for b in self._breeder_db if b["id"] == breeder_id), None)
        if not target:
            return []
            
        similar = []
        for breeder in self._breeder_db:
            if breeder["id"] == breeder_id:
                continue
            # Similar if shared specialties
            shared = set(target.get("specialties", [])) & set(breeder.get("specialties", []))
            if shared:
                similar.append({"name": breeder["name"], "shared_specialty": list(shared)[0]})
                
        return similar[:3]


# Register agent
AgentRegistry.register(BreederSpotlightAgent())
