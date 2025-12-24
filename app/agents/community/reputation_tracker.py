"""
Reputation Tracker Agent

Tracks and manages community reputation, trust scores, and achievements.

Part of Community Agents.
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


class ReputationTier(str, Enum):
    """Reputation tiers based on score"""
    LEGENDARY = "legendary"    # 10000+
    CHAMPION = "champion"      # 5000-9999
    EXPERT = "expert"          # 2500-4999
    VETERAN = "veteran"        # 1000-2499
    ESTABLISHED = "established"  # 500-999
    RISING = "rising"          # 100-499
    NEWCOMER = "newcomer"      # 0-99


class ReputationCategory(str, Enum):
    """Categories that contribute to reputation"""
    GROWING = "growing"
    HELPING = "helping"
    TRADING = "trading"
    CONTENT = "content"
    ENGAGEMENT = "engagement"


class ReputationAction(str, Enum):
    """Actions that affect reputation"""
    GROW_COMPLETE = "grow_complete"
    HELP_ANSWER = "help_answer"
    ANSWER_ACCEPTED = "answer_accepted"
    TRADE_COMPLETE = "trade_complete"
    POSITIVE_REVIEW = "positive_review"
    NEGATIVE_REVIEW = "negative_review"
    CONTENT_POSTED = "content_posted"
    CONTENT_LIKED = "content_liked"
    MENTOR_SESSION = "mentor_session"
    DAILY_CHECKIN = "daily_checkin"


# Reputation points per action
REPUTATION_POINTS = {
    ReputationAction.GROW_COMPLETE: 100,
    ReputationAction.HELP_ANSWER: 10,
    ReputationAction.ANSWER_ACCEPTED: 25,
    ReputationAction.TRADE_COMPLETE: 50,
    ReputationAction.POSITIVE_REVIEW: 15,
    ReputationAction.NEGATIVE_REVIEW: -30,
    ReputationAction.CONTENT_POSTED: 5,
    ReputationAction.CONTENT_LIKED: 2,
    ReputationAction.MENTOR_SESSION: 75,
    ReputationAction.DAILY_CHECKIN: 1,
}


class ReputationProfile(BaseModel):
    """User's reputation profile"""
    user_id: int
    total_score: int = 0
    tier: ReputationTier = ReputationTier.NEWCOMER
    category_scores: Dict[str, int] = Field(default_factory=dict)
    badges: List[str] = Field(default_factory=list)
    trust_level: float = Field(default=0.5, ge=0, le=1)
    member_since: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)


class ReputationTrackerAgent(BaseAgent):
    """
    Community reputation and trust tracking agent.
    
    Capabilities:
    - Track reputation scores
    - Award/deduct reputation points  
    - Manage trust levels
    - Verify seller/breeder reputation
    - Generate reputation reports
    
    Integrates with:
    - Gamification engine
    - Marketplace (seller trust)
    - Community features
    """
    
    def __init__(self):
        super().__init__(
            agent_id="reputation_tracker",
            name="Reputation Tracker",
            role=AgentRole.COMMUNITY,
            description="Community reputation, trust scores, and verification",
        )
        
        # Register MCP tools
        self.register_tool(
            "get_reputation",
            self.get_reputation,
            "Get user's reputation profile"
        )
        self.register_tool(
            "award_reputation",
            self.award_reputation,
            "Award reputation points for an action"
        )
        self.register_tool(
            "get_leaderboard",
            self.get_leaderboard,
            "Get reputation leaderboard"
        )
        self.register_tool(
            "verify_seller",
            self.verify_seller_trust,
            "Verify seller's trust level for marketplace"
        )
        self.register_tool(
            "get_badges",
            self.get_available_badges,
            "Get available reputation badges"
        )
        
        # Mock reputation database
        self._reputations: Dict[int, Dict] = {}
        
    async def execute(self, context: AgentContext, **kwargs) -> AgentResult:
        """Execute reputation tracking operation"""
        action = kwargs.get("action", "get")
        
        try:
            if action == "get":
                result = await self.get_reputation(
                    user_id=kwargs.get("user_id") or context.user_id,
                )
            elif action == "award":
                result = await self.award_reputation(
                    user_id=kwargs.get("user_id") or context.user_id,
                    rep_action=kwargs.get("rep_action"),
                    category=kwargs.get("category", "engagement"),
                    details=kwargs.get("details"),
                )
            elif action == "leaderboard":
                result = await self.get_leaderboard(
                    category=kwargs.get("category"),
                    limit=kwargs.get("limit", 10),
                )
            elif action == "verify":
                result = await self.verify_seller_trust(
                    user_id=kwargs.get("user_id"),
                )
            elif action == "badges":
                result = await self.get_available_badges(
                    user_id=kwargs.get("user_id") or context.user_id,
                )
            else:
                result = {"error": f"Unknown action: {action}"}
                
            return AgentResult(
                success=True,
                agent_id=self.agent_id,
                output=result,
                confidence=0.95,
                xp_reward=2,
                next_actions=["view_leaderboard", "earn_more", "claim_badge"],
            )
            
        except Exception as e:
            logger.error(f"ReputationTracker error: {e}")
            return AgentResult(
                success=False,
                agent_id=self.agent_id,
                output=None,
                error=str(e),
            )
    
    async def get_reputation(self, user_id: Optional[int]) -> Dict[str, Any]:
        """Get user's reputation profile"""
        if not user_id:
            return {"error": "user_id required"}
            
        # Get or create reputation
        rep = self._get_or_create_reputation(user_id)
        tier = self._calculate_tier(rep["total_score"])
        
        return {
            "user_id": user_id,
            "total_score": rep["total_score"],
            "tier": tier.value,
            "tier_emoji": self._get_tier_emoji(tier),
            "category_breakdown": rep["category_scores"],
            "badges": rep["badges"],
            "trust_level": rep["trust_level"],
            "rank": self._get_rank(user_id),
            "next_tier": self._get_next_tier_info(rep["total_score"]),
            "recent_activity": rep.get("recent_actions", [])[-5:],
            "member_since": rep.get("member_since", datetime.utcnow().isoformat()),
        }
    
    async def award_reputation(
        self,
        user_id: Optional[int],
        rep_action: Optional[str],
        category: str = "engagement",
        details: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Award reputation points for an action"""
        if not user_id:
            return {"error": "user_id required"}
        if not rep_action:
            return {"error": "rep_action required"}
            
        try:
            action_enum = ReputationAction(rep_action)
        except ValueError:
            return {"error": f"Invalid action: {rep_action}", "valid_actions": [a.value for a in ReputationAction]}
            
        points = REPUTATION_POINTS.get(action_enum, 0)
        
        # Update reputation
        rep = self._get_or_create_reputation(user_id)
        rep["total_score"] += points
        
        # Update category
        if category not in rep["category_scores"]:
            rep["category_scores"][category] = 0
        rep["category_scores"][category] += max(0, points)  # Categories only track positive
        
        # Update trust level based on actions
        if points > 0:
            rep["trust_level"] = min(1.0, rep["trust_level"] + 0.01)
        elif points < 0:
            rep["trust_level"] = max(0.0, rep["trust_level"] - 0.05)
            
        # Log action
        if "recent_actions" not in rep:
            rep["recent_actions"] = []
        rep["recent_actions"].append({
            "action": rep_action,
            "points": points,
            "timestamp": datetime.utcnow().isoformat(),
            "details": details,
        })
        
        # Check for tier upgrade
        old_tier = rep.get("tier", ReputationTier.NEWCOMER)
        new_tier = self._calculate_tier(rep["total_score"])
        tier_upgraded = old_tier != new_tier
        rep["tier"] = new_tier
        
        # Check for badges
        new_badges = self._check_badge_eligibility(rep)
        
        self._reputations[user_id] = rep
        
        return {
            "success": True,
            "user_id": user_id,
            "action": rep_action,
            "points_awarded": points,
            "new_total": rep["total_score"],
            "tier": new_tier.value,
            "tier_upgraded": tier_upgraded,
            "new_badges": new_badges,
            "trust_level": round(rep["trust_level"], 2),
        }
    
    async def get_leaderboard(
        self,
        category: Optional[str] = None,
        limit: int = 10,
    ) -> Dict[str, Any]:
        """Get reputation leaderboard"""
        
        # Sort users by score
        if category:
            sorted_users = sorted(
                self._reputations.items(),
                key=lambda x: x[1].get("category_scores", {}).get(category, 0),
                reverse=True
            )
        else:
            sorted_users = sorted(
                self._reputations.items(),
                key=lambda x: x[1].get("total_score", 0),
                reverse=True
            )
            
        leaderboard = []
        for rank, (user_id, rep) in enumerate(sorted_users[:limit], 1):
            tier = self._calculate_tier(rep.get("total_score", 0))
            leaderboard.append({
                "rank": rank,
                "user_id": user_id,
                "score": rep.get("total_score", 0) if not category else rep.get("category_scores", {}).get(category, 0),
                "tier": tier.value,
                "tier_emoji": self._get_tier_emoji(tier),
                "badges_count": len(rep.get("badges", [])),
            })
            
        # Add mock users if leaderboard is empty
        if not leaderboard:
            leaderboard = [
                {"rank": 1, "user_id": 1, "score": 5500, "tier": "champion", "tier_emoji": "🏆", "badges_count": 12},
                {"rank": 2, "user_id": 2, "score": 3200, "tier": "expert", "tier_emoji": "🎖️", "badges_count": 8},
                {"rank": 3, "user_id": 3, "score": 1800, "tier": "veteran", "tier_emoji": "⭐", "badges_count": 5},
            ]
            
        return {
            "category": category or "overall",
            "period": "all_time",
            "leaderboard": leaderboard,
            "your_rank": "Not ranked yet",  # Would calculate for current user
            "categories": [c.value for c in ReputationCategory],
        }
    
    async def verify_seller_trust(self, user_id: Optional[int]) -> Dict[str, Any]:
        """Verify seller's trust level for marketplace transactions"""
        if not user_id:
            return {"error": "user_id required"}
            
        rep = self._get_or_create_reputation(user_id)
        trust = rep.get("trust_level", 0.5)
        tier = self._calculate_tier(rep.get("total_score", 0))
        
        # Calculate trust grade
        if trust >= 0.9:
            trust_grade = "A+"
            recommendation = "Highly trusted seller - safe to transact"
        elif trust >= 0.8:
            trust_grade = "A"
            recommendation = "Trusted seller with strong track record"
        elif trust >= 0.7:
            trust_grade = "B"
            recommendation = "Good reputation - proceed with confidence"
        elif trust >= 0.5:
            trust_grade = "C"
            recommendation = "Building reputation - consider escrow"
        else:
            trust_grade = "D"
            recommendation = "New or low reputation - use caution"
            
        trading_score = rep.get("category_scores", {}).get("trading", 0)
        
        return {
            "user_id": user_id,
            "trust_level": round(trust, 2),
            "trust_grade": trust_grade,
            "reputation_tier": tier.value,
            "trading_score": trading_score,
            "recommendation": recommendation,
            "verified_badges": [b for b in rep.get("badges", []) if "verified" in b.lower()],
            "total_trades": trading_score // 50,  # Rough estimate
            "member_since": rep.get("member_since", "Unknown"),
            "warnings": [] if trust >= 0.5 else ["Low trust score - review history"],
        }
    
    async def get_available_badges(self, user_id: Optional[int]) -> Dict[str, Any]:
        """Get badges and achievement status"""
        if not user_id:
            return {"error": "user_id required"}
            
        rep = self._get_or_create_reputation(user_id)
        earned_badges = set(rep.get("badges", []))
        
        all_badges = [
            {"id": "first_grow", "name": "First Harvest", "description": "Complete your first grow", "points": 100, "category": "growing"},
            {"id": "helpful_10", "name": "Helpful Hand", "description": "Answer 10 community questions", "points": 50, "category": "helping"},
            {"id": "trader_5", "name": "Trusted Trader", "description": "Complete 5 marketplace trades", "points": 75, "category": "trading"},
            {"id": "content_creator", "name": "Content Creator", "description": "Post 20 pieces of content", "points": 60, "category": "content"},
            {"id": "streak_30", "name": "Dedicated Grower", "description": "30-day check-in streak", "points": 150, "category": "engagement"},
            {"id": "mentor", "name": "Community Mentor", "description": "Help 5 growers as a mentor", "points": 200, "category": "helping"},
            {"id": "verified_seller", "name": "Verified Seller", "description": "Achieve 0.9+ trust level", "points": 100, "category": "trading"},
            {"id": "expert_tier", "name": "Expert Status", "description": "Reach Expert reputation tier", "points": 500, "category": "engagement"},
        ]
        
        badges_status = []
        for badge in all_badges:
            is_earned = badge["id"] in earned_badges
            badges_status.append({
                **badge,
                "earned": is_earned,
                "earned_date": datetime.utcnow().isoformat() if is_earned else None,
            })
            
        return {
            "user_id": user_id,
            "total_badges": len([b for b in badges_status if b["earned"]]),
            "total_available": len(all_badges),
            "badges": badges_status,
            "next_badge": next((b for b in badges_status if not b["earned"]), None),
        }
    
    def _get_or_create_reputation(self, user_id: int) -> Dict:
        """Get or create reputation record"""
        if user_id not in self._reputations:
            self._reputations[user_id] = {
                "total_score": 0,
                "tier": ReputationTier.NEWCOMER,
                "category_scores": {},
                "badges": [],
                "trust_level": 0.5,
                "member_since": datetime.utcnow().isoformat(),
                "recent_actions": [],
            }
        return self._reputations[user_id]
    
    def _calculate_tier(self, score: int) -> ReputationTier:
        """Calculate tier based on score"""
        if score >= 10000:
            return ReputationTier.LEGENDARY
        elif score >= 5000:
            return ReputationTier.CHAMPION
        elif score >= 2500:
            return ReputationTier.EXPERT
        elif score >= 1000:
            return ReputationTier.VETERAN
        elif score >= 500:
            return ReputationTier.ESTABLISHED
        elif score >= 100:
            return ReputationTier.RISING
        return ReputationTier.NEWCOMER
    
    def _get_tier_emoji(self, tier: ReputationTier) -> str:
        """Get emoji for tier"""
        emojis = {
            ReputationTier.LEGENDARY: "👑",
            ReputationTier.CHAMPION: "🏆",
            ReputationTier.EXPERT: "🎖️",
            ReputationTier.VETERAN: "⭐",
            ReputationTier.ESTABLISHED: "💫",
            ReputationTier.RISING: "🌱",
            ReputationTier.NEWCOMER: "🆕",
        }
        return emojis.get(tier, "")
    
    def _get_next_tier_info(self, score: int) -> Dict[str, Any]:
        """Get info about next tier"""
        thresholds = [
            (100, ReputationTier.RISING),
            (500, ReputationTier.ESTABLISHED),
            (1000, ReputationTier.VETERAN),
            (2500, ReputationTier.EXPERT),
            (5000, ReputationTier.CHAMPION),
            (10000, ReputationTier.LEGENDARY),
        ]
        
        for threshold, tier in thresholds:
            if score < threshold:
                return {
                    "tier": tier.value,
                    "points_needed": threshold - score,
                    "progress_percent": round((score / threshold) * 100, 1),
                }
        return {"tier": "max", "points_needed": 0, "progress_percent": 100}
    
    def _get_rank(self, user_id: int) -> int:
        """Get user's rank among all users"""
        sorted_users = sorted(
            self._reputations.items(),
            key=lambda x: x[1].get("total_score", 0),
            reverse=True
        )
        for rank, (uid, _) in enumerate(sorted_users, 1):
            if uid == user_id:
                return rank
        return len(sorted_users) + 1
    
    def _check_badge_eligibility(self, rep: Dict) -> List[str]:
        """Check if user earned any new badges"""
        new_badges = []
        existing_badges = set(rep.get("badges", []))
        
        # Check various badge conditions
        if rep.get("total_score", 0) >= 2500 and "expert_tier" not in existing_badges:
            new_badges.append("expert_tier")
            
        if rep.get("trust_level", 0) >= 0.9 and "verified_seller" not in existing_badges:
            new_badges.append("verified_seller")
            
        # Add new badges
        rep["badges"] = list(existing_badges | set(new_badges))
        
        return new_badges


# Register agent
AgentRegistry.register(ReputationTrackerAgent())
