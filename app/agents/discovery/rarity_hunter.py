"""
Rarity Hunter Agent

Finds rare and limited genetics, drop alerts, and collectability scoring.

Part of Discovery Agents.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
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


class RarityTier(str, Enum):
    """Strain rarity tiers"""
    MYTHIC = "mythic"
    LEGENDARY = "legendary"
    EPIC = "epic"
    RARE = "rare"
    UNCOMMON = "uncommon"
    COMMON = "common"


class DropType(str, Enum):
    """Types of seed drops"""
    EXCLUSIVE = "exclusive"
    LIMITED_EDITION = "limited_edition"
    COLLABORATION = "collaboration"
    RESTOCK = "restock"
    REGULAR = "regular"


class RareStrain(BaseModel):
    """Rare strain information"""
    id: int
    name: str
    breeder: str
    rarity_tier: RarityTier
    rarity_score: float = Field(ge=0, le=100)
    availability: str
    last_drop: Optional[datetime] = None
    next_drop: Optional[datetime] = None
    estimated_value: Optional[float] = None
    nft_linked: bool = False


class DropAlert(BaseModel):
    """Upcoming drop alert"""
    strain_name: str
    breeder: str
    drop_type: DropType
    drop_date: datetime
    estimated_quantity: Optional[int] = None
    price_estimate: Optional[float] = None


class RarityHunterAgent(BaseAgent):
    """
    Rare genetics discovery and alert agent.
    
    Capabilities:
    - Rare strain discovery and scoring
    - Upcoming drop alerts
    - Limited edition tracking
    - Collectability analysis
    - NFT-linked genetics
    
    Integrates with:
    - Strain marketplace data
    - NFT verification (Algorand)
    - Gamification (XP for rare finds)
    """
    
    def __init__(self):
        super().__init__(
            agent_id="rarity_hunter",
            name="Rarity Hunter",
            role=AgentRole.DISCOVERY,
            description="Rare genetics discovery and drop alerts",
        )
        
        # Register MCP tools
        self.register_tool(
            "find_rare",
            self.find_rare_strains,
            "Find rare and limited strains"
        )
        self.register_tool(
            "get_drops",
            self.get_upcoming_drops,
            "Get upcoming drop alerts"
        )
        self.register_tool(
            "calculate_rarity",
            self.calculate_rarity_score,
            "Calculate rarity score for strain"
        )
        self.register_tool(
            "get_collectibles",
            self.get_nft_collectibles,
            "Get NFT-linked collectible strains"
        )
        self.register_tool(
            "set_alert",
            self.set_drop_alert,
            "Set alert for specific drop"
        )
        
        # Mock rare strains database
        self._rare_db = self._load_mock_rare_strains()
        self._user_alerts: Dict[int, List[Dict]] = {}  # user_id -> alerts
        
    async def execute(self, context: AgentContext, **kwargs) -> AgentResult:
        """Execute rarity hunting"""
        action = kwargs.get("action", "find")
        
        try:
            if action == "find":
                result = await self.find_rare_strains(
                    min_rarity=kwargs.get("min_rarity", "rare"),
                    breeder=kwargs.get("breeder"),
                    limit=kwargs.get("limit", 10),
                )
            elif action == "drops":
                result = await self.get_upcoming_drops(
                    days_ahead=kwargs.get("days_ahead", 30),
                )
            elif action == "score":
                result = await self.calculate_rarity_score(
                    strain_id=kwargs.get("strain_id"),
                )
            elif action == "collectibles":
                result = await self.get_nft_collectibles()
            elif action == "alert":
                result = await self.set_drop_alert(
                    user_id=context.user_id,
                    strain_name=kwargs.get("strain_name"),
                    breeder=kwargs.get("breeder"),
                )
            else:
                result = {"error": f"Unknown action: {action}"}
                
            # Award bonus XP for rare finds
            xp_reward = 10 if action == "find" else 5
            if context.user_id:
                gamification_engine.award_xp(
                    context.user_id, xp_reward, "rarity_hunting"
                )
                
            return AgentResult(
                success=True,
                agent_id=self.agent_id,
                output=result,
                confidence=0.88,
                xp_reward=xp_reward,
                next_actions=["set_alert", "view_details", "add_to_wishlist"],
            )
            
        except Exception as e:
            logger.error(f"RarityHunter error: {e}")
            return AgentResult(
                success=False,
                agent_id=self.agent_id,
                output=None,
                error=str(e),
            )
    
    async def find_rare_strains(
        self,
        min_rarity: str = "rare",
        breeder: Optional[str] = None,
        limit: int = 10,
    ) -> Dict[str, Any]:
        """Find rare and limited strains"""
        # Map rarity to minimum score
        rarity_scores = {
            "common": 0,
            "uncommon": 20,
            "rare": 40,
            "epic": 60,
            "legendary": 80,
            "mythic": 95,
        }
        min_score = rarity_scores.get(min_rarity.lower(), 40)
        
        # Filter strains
        filtered = [
            s for s in self._rare_db
            if s["rarity_score"] >= min_score
        ]
        
        if breeder:
            filtered = [s for s in filtered if breeder.lower() in s["breeder"].lower()]
            
        # Sort by rarity score
        filtered.sort(key=lambda x: x["rarity_score"], reverse=True)
        
        return {
            "search_criteria": {
                "min_rarity": min_rarity,
                "breeder_filter": breeder,
            },
            "total_found": len(filtered),
            "rare_strains": filtered[:limit],
            "rarity_breakdown": self._get_rarity_breakdown(),
            "tips": [
                "Set alerts for strains you want - they sell out fast!",
                "Check 'upcoming drops' for restock notifications",
                "NFT-linked strains may have additional perks",
            ],
        }
    
    async def get_upcoming_drops(self, days_ahead: int = 30) -> Dict[str, Any]:
        """Get upcoming drop alerts"""
        now = datetime.utcnow()
        cutoff = now + timedelta(days=days_ahead)
        
        # Mock upcoming drops
        drops = [
            {
                "strain_name": "Midnight Express",
                "breeder": "Night Owl Seeds",
                "drop_type": DropType.LIMITED_EDITION.value,
                "drop_date": (now + timedelta(days=3)).isoformat(),
                "estimated_quantity": 500,
                "price_estimate": 80.00,
                "rarity_tier": RarityTier.LEGENDARY.value,
                "hype_score": 9.2,
            },
            {
                "strain_name": "Double Grape",
                "breeder": "Mephisto Genetics",
                "drop_type": DropType.RESTOCK.value,
                "drop_date": (now + timedelta(days=7)).isoformat(),
                "estimated_quantity": 1000,
                "price_estimate": 50.00,
                "rarity_tier": RarityTier.EPIC.value,
                "hype_score": 8.5,
            },
            {
                "strain_name": "Founder's Cut #1",
                "breeder": "CultivAR Genetics",
                "drop_type": DropType.EXCLUSIVE.value,
                "drop_date": (now + timedelta(days=14)).isoformat(),
                "estimated_quantity": 100,
                "price_estimate": 150.00,
                "rarity_tier": RarityTier.MYTHIC.value,
                "hype_score": 10.0,
                "nft_required": True,
            },
        ]
        
        return {
            "period": f"Next {days_ahead} days",
            "total_drops": len(drops),
            "drops": drops,
            "drop_calendar": self._generate_calendar(drops),
            "hot_tip": "🔥 Founder's Cut #1 requires Founder NFT - extremely limited!",
        }
    
    async def calculate_rarity_score(self, strain_id: Optional[int] = None) -> Dict[str, Any]:
        """Calculate detailed rarity score for strain"""
        if strain_id is None:
            return {"error": "strain_id required"}
            
        strain = next((s for s in self._rare_db if s["id"] == strain_id), None)
        
        if not strain:
            return {"error": f"Strain {strain_id} not found"}
            
        # Detailed scoring breakdown
        scoring = {
            "availability_score": self._score_availability(strain),
            "demand_score": self._score_demand(strain),
            "breeder_prestige": self._score_breeder(strain),
            "genetics_uniqueness": self._score_genetics(strain),
            "collectability": self._score_collectability(strain),
        }
        
        total_score = sum(scoring.values()) / len(scoring)
        tier = self._score_to_tier(total_score)
        
        return {
            "strain": strain["name"],
            "overall_rarity_score": round(total_score, 1),
            "rarity_tier": tier.value,
            "score_breakdown": scoring,
            "factors": {
                "positive": self._get_positive_factors(strain),
                "negative": self._get_negative_factors(strain),
            },
            "market_insight": self._get_market_insight(strain, total_score),
        }
    
    async def get_nft_collectibles(self) -> Dict[str, Any]:
        """Get NFT-linked collectible strains"""
        nft_strains = [s for s in self._rare_db if s.get("nft_linked", False)]
        
        return {
            "total_nft_linked": len(nft_strains),
            "nft_collectibles": nft_strains,
            "benefits": [
                "Exclusive access to limited drops",
                "Discounts on future releases",
                "Verified authenticity on Algorand",
                "Tradeable digital provenance",
            ],
            "how_to_get": [
                "Purchase Founder NFT from marketplace",
                "Win NFTs in community events",
                "Some strains include free NFT",
            ],
        }
    
    async def set_drop_alert(
        self,
        user_id: Optional[int],
        strain_name: Optional[str],
        breeder: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Set alert for specific drop"""
        if not user_id:
            return {"error": "User ID required for alerts"}
        if not strain_name:
            return {"error": "strain_name required"}
            
        alert = {
            "strain_name": strain_name,
            "breeder": breeder,
            "created_at": datetime.utcnow().isoformat(),
            "active": True,
        }
        
        if user_id not in self._user_alerts:
            self._user_alerts[user_id] = []
            
        self._user_alerts[user_id].append(alert)
        
        return {
            "success": True,
            "message": f"Alert set for {strain_name}",
            "alert": alert,
            "total_alerts": len(self._user_alerts[user_id]),
            "notification_methods": ["push", "email", "in-app"],
        }
    
    def _load_mock_rare_strains(self) -> List[Dict]:
        """Load mock rare strains database"""
        return [
            {
                "id": 101,
                "name": "Galaxy Brain",
                "breeder": "Night Owl Seeds",
                "rarity_tier": RarityTier.MYTHIC.value,
                "rarity_score": 98,
                "availability": "Sold out - Last drop 6 months ago",
                "estimated_value": 200.00,
                "nft_linked": True,
            },
            {
                "id": 102,
                "name": "Wizard's Apprentice",
                "breeder": "Mephisto Genetics",
                "rarity_tier": RarityTier.LEGENDARY.value,
                "rarity_score": 88,
                "availability": "Limited - Occasional restocks",
                "estimated_value": 120.00,
                "nft_linked": False,
            },
            {
                "id": 103,
                "name": "Cosmic Queen",
                "breeder": "Mephisto Genetics",
                "rarity_tier": RarityTier.EPIC.value,
                "rarity_score": 72,
                "availability": "Rare - Quarterly drops",
                "estimated_value": 80.00,
                "nft_linked": False,
            },
            {
                "id": 104,
                "name": "Forum Stomper",
                "breeder": "Mephisto Genetics",
                "rarity_tier": RarityTier.RARE.value,
                "rarity_score": 55,
                "availability": "Available - Regular stock",
                "estimated_value": 50.00,
                "nft_linked": False,
            },
        ]
    
    def _get_rarity_breakdown(self) -> Dict[str, int]:
        """Get count by rarity tier"""
        breakdown = {}
        for strain in self._rare_db:
            tier = strain["rarity_tier"]
            breakdown[tier] = breakdown.get(tier, 0) + 1
        return breakdown
    
    def _generate_calendar(self, drops: List[Dict]) -> List[Dict]:
        """Generate drop calendar"""
        calendar = []
        for drop in sorted(drops, key=lambda x: x["drop_date"]):
            calendar.append({
                "date": drop["drop_date"][:10],
                "event": f"{drop['breeder']} - {drop['strain_name']}",
                "type": drop["drop_type"],
            })
        return calendar
    
    def _score_availability(self, strain: Dict) -> float:
        """Score based on availability"""
        if "sold out" in strain.get("availability", "").lower():
            return 95
        elif "limited" in strain.get("availability", "").lower():
            return 75
        elif "rare" in strain.get("availability", "").lower():
            return 60
        return 30
    
    def _score_demand(self, strain: Dict) -> float:
        """Score based on demand"""
        # Mock - would use real market data
        return strain.get("rarity_score", 50) * 0.9
    
    def _score_breeder(self, strain: Dict) -> float:
        """Score based on breeder prestige"""
        prestige = {
            "Night Owl Seeds": 95,
            "Mephisto Genetics": 90,
            "Ethos Genetics": 85,
        }
        return prestige.get(strain.get("breeder", ""), 50)
    
    def _score_genetics(self, strain: Dict) -> float:
        """Score based on genetic uniqueness"""
        return strain.get("rarity_score", 50)
    
    def _score_collectability(self, strain: Dict) -> float:
        """Score based on collectability"""
        score = 50
        if strain.get("nft_linked"):
            score += 30
        if strain.get("rarity_tier") in [RarityTier.MYTHIC.value, RarityTier.LEGENDARY.value]:
            score += 20
        return min(score, 100)
    
    def _score_to_tier(self, score: float) -> RarityTier:
        """Convert score to rarity tier"""
        if score >= 95:
            return RarityTier.MYTHIC
        elif score >= 80:
            return RarityTier.LEGENDARY
        elif score >= 60:
            return RarityTier.EPIC
        elif score >= 40:
            return RarityTier.RARE
        elif score >= 20:
            return RarityTier.UNCOMMON
        return RarityTier.COMMON
    
    def _get_positive_factors(self, strain: Dict) -> List[str]:
        """Get positive rarity factors"""
        factors = []
        if strain.get("nft_linked"):
            factors.append("NFT-verified authenticity")
        if strain.get("rarity_tier") == RarityTier.MYTHIC.value:
            factors.append("Extremely limited release")
        if "Night Owl" in strain.get("breeder", ""):
            factors.append("Highly sought-after breeder")
        return factors if factors else ["Quality genetics"]
    
    def _get_negative_factors(self, strain: Dict) -> List[str]:
        """Get negative rarity factors"""
        if "available" in strain.get("availability", "").lower():
            return ["Regular availability reduces collectability"]
        return []
    
    def _get_market_insight(self, strain: Dict, score: float) -> str:
        """Get market insight for strain"""
        if score >= 90:
            return "🔥 Highly collectible - expect high demand at any drop"
        elif score >= 70:
            return "📈 Strong collector interest - set alerts for restocks"
        else:
            return "👍 Solid choice - good availability for new growers"


# Register agent
AgentRegistry.register(RarityHunterAgent())
