"""
Daily Check-In Agent

Gamified daily status updates with XP rewards.
Tracks streaks and provides personalized insights.

Part of Growing Agents.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import logging

from ..base import (
    AgentRole,
    AgentContext,
    AgentResult,
    BaseAgent,
    AgentRegistry,
)
from ...gamification import gamification_engine

logger = logging.getLogger(__name__)


@dataclass
class DailyCheckInData:
    """Data collected during daily check-in"""
    plant_ids: List[int]
    observations: Dict[int, str]  # plant_id -> observation
    photos_uploaded: int
    issues_reported: List[str]
    environment_logged: bool
    notes: str


class DailyCheckInAgent(BaseAgent):
    """
    Gamified daily check-in agent.
    
    Features:
    - Quick plant status updates
    - Streak tracking with bonus XP
    - Personalized tips based on grow stage
    - Integration with other agents for intelligent responses
    """
    
    def __init__(self):
        super().__init__(
            agent_id="daily_checkin",
            name="Daily Check-In",
            role=AgentRole.GROWING,
            description="Gamified daily status updates with streak tracking",
        )
        
        # Register MCP tools
        self.register_tool(
            "start_checkin",
            self.start_checkin,
            "Start a daily check-in session"
        )
        self.register_tool(
            "submit_checkin",
            self.submit_checkin,
            "Submit daily check-in data"
        )
        self.register_tool(
            "get_streak_status",
            self.get_streak_status,
            "Get current streak status and rewards"
        )
        
    async def execute(self, context: AgentContext, **kwargs) -> AgentResult:
        """Execute daily check-in"""
        action = kwargs.get("action", "start")
        
        try:
            if action == "start":
                result = await self.start_checkin(context.user_id)
            elif action == "submit":
                result = await self.submit_checkin(
                    user_id=context.user_id,
                    checkin_data=kwargs.get("checkin_data", {}),
                )
            elif action == "streak":
                result = await self.get_streak_status(context.user_id)
            else:
                result = {"error": f"Unknown action: {action}"}
                
            return AgentResult(
                success=True,
                agent_id=self.agent_id,
                output=result,
                confidence=1.0,
                xp_reward=result.get("xp_earned", 0),
            )
            
        except Exception as e:
            logger.error(f"DailyCheckIn error: {e}")
            return AgentResult(
                success=False,
                agent_id=self.agent_id,
                output=None,
                error=str(e),
            )
    
    async def start_checkin(self, user_id: int) -> Dict[str, Any]:
        """Start a daily check-in session"""
        
        progress = gamification_engine.get_user_progress(user_id)
        
        # Check if already checked in today
        now = datetime.utcnow()
        already_checked_in = (
            progress.last_checkin and 
            progress.last_checkin.date() == now.date()
        )
        
        # Get plants needing check-in (mock data)
        plants_to_check = [
            {"id": 1, "name": "Blue Dream #1", "stage": "flowering", "day": 42},
            {"id": 2, "name": "GSC #1", "stage": "flowering", "day": 38},
            {"id": 3, "name": "Purple Punch #1", "stage": "vegetative", "day": 21},
        ]
        
        # Get tips based on grow stage
        tips = self._get_stage_tips(plants_to_check)
        
        return {
            "already_checked_in": already_checked_in,
            "current_streak": progress.current_streak,
            "streak_bonus_xp": min(progress.current_streak * 2, 50),
            "plants_to_check": plants_to_check,
            "quick_tips": tips,
            "checkin_prompt": self._generate_prompt(plants_to_check),
        }
    
    async def submit_checkin(
        self,
        user_id: int,
        checkin_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Submit daily check-in and award XP"""
        
        # Process check-in with gamification engine
        checkin_result = gamification_engine.daily_checkin(user_id)
        
        if checkin_result.get("already_checked_in"):
            return {
                "success": False,
                "message": "You've already checked in today!",
                "streak": checkin_result.get("streak", 0),
            }
        
        # Calculate bonus XP for thorough check-in
        bonus_xp = 0
        
        # Bonus for adding observations
        observations = checkin_data.get("observations", {})
        if observations:
            bonus_xp += min(len(observations) * 5, 25)  # Up to 25 XP
            
        # Bonus for uploading photos
        photos = checkin_data.get("photos_uploaded", 0)
        if photos > 0:
            bonus_xp += min(photos * 10, 30)  # Up to 30 XP
            
        # Bonus for logging environment
        if checkin_data.get("environment_logged"):
            bonus_xp += 10
            
        # Award bonus XP
        if bonus_xp > 0:
            gamification_engine.award_xp(user_id, bonus_xp, "checkin_bonus")
            
        total_xp = checkin_result.get("xp_earned", 0) + bonus_xp
        
        # Generate personalized insights
        insights = self._generate_insights(checkin_data)
        
        return {
            "success": True,
            "message": "Check-in complete! 🎉",
            "streak": checkin_result.get("current_streak", 1),
            "longest_streak": checkin_result.get("longest_streak", 1),
            "base_xp": checkin_result.get("xp_earned", 0),
            "bonus_xp": bonus_xp,
            "total_xp": total_xp,
            "xp_earned": total_xp,
            "level": checkin_result.get("level", 1),
            "level_up": checkin_result.get("level_up", False),
            "achievements_unlocked": checkin_result.get("achievements_unlocked", []),
            "insights": insights,
            "next_milestone": self._get_next_streak_milestone(
                checkin_result.get("current_streak", 1)
            ),
        }
    
    async def get_streak_status(self, user_id: int) -> Dict[str, Any]:
        """Get current streak status"""
        
        progress = gamification_engine.get_user_progress(user_id)
        
        next_milestone = self._get_next_streak_milestone(progress.current_streak)
        
        return {
            "current_streak": progress.current_streak,
            "longest_streak": progress.longest_streak,
            "streak_bonus": min(progress.current_streak * 2, 50),
            "next_milestone": next_milestone,
            "days_to_next": next_milestone["days"] - progress.current_streak,
            "streak_achievements": self._get_streak_achievements(progress),
        }
    
    def _get_stage_tips(self, plants: List[Dict]) -> List[str]:
        """Get tips based on plant stages"""
        tips = []
        
        stages = {p.get("stage") for p in plants}
        
        if "flowering" in stages:
            tips.extend([
                "🌸 Check trichome development on flowering plants",
                "💧 Reduce nitrogen as plants mature in flower",
                "🌡️ Keep temps 75-82°F for optimal resin production",
            ])
            
        if "vegetative" in stages:
            tips.extend([
                "🌱 Vegetative plants love high nitrogen feeds",
                "✂️ Consider topping or LST for bushier growth",
                "💡 18/6 light schedule optimal for veg",
            ])
            
        return tips[:3]  # Return top 3 tips
    
    def _generate_prompt(self, plants: List[Dict]) -> str:
        """Generate personalized check-in prompt"""
        
        if not plants:
            return "Ready to start tracking your grow?"
            
        flowering = [p for p in plants if p.get("stage") == "flowering"]
        
        if flowering:
            days = [p.get("day", 0) for p in flowering]
            avg_day = sum(days) / len(days)
            
            if avg_day > 50:
                return "🔍 Your flowering plants are maturing! Check those trichomes!"
            elif avg_day > 30:
                return "🌸 Flower development in full swing! How are the buds looking?"
            else:
                return "🌼 Early flower - watch for bud site development!"
                
        return "How are your plants looking today? 🌱"
    
    def _generate_insights(self, checkin_data: Dict) -> List[str]:
        """Generate insights based on check-in data"""
        insights = []
        
        observations = checkin_data.get("observations", {})
        
        # Look for keywords in observations
        for plant_id, obs in observations.items():
            obs_lower = obs.lower()
            
            if "yellow" in obs_lower:
                insights.append(
                    f"🔍 Yellowing noted on plant {plant_id} - "
                    "consider checking pH and nitrogen levels"
                )
            elif "curl" in obs_lower:
                insights.append(
                    f"🌡️ Leaf curl on plant {plant_id} - "
                    "check for heat stress or overwatering"
                )
            elif "great" in obs_lower or "good" in obs_lower:
                insights.append(
                    f"✨ Plant {plant_id} is thriving! Keep up the good work!"
                )
                
        if not insights:
            insights.append("📊 Keep logging daily for better pattern detection!")
            
        return insights
    
    def _get_next_streak_milestone(self, current_streak: int) -> Dict[str, Any]:
        """Get next streak milestone"""
        milestones = [
            {"days": 7, "name": "Week Warrior", "reward": "50 XP + Badge"},
            {"days": 14, "name": "Two Week Trek", "reward": "75 XP"},
            {"days": 30, "name": "Monthly Master", "reward": "200 XP + NFT"},
            {"days": 60, "name": "Dedicated Grower", "reward": "500 XP"},
            {"days": 100, "name": "Century Club", "reward": "1000 XP + Exclusive NFT"},
        ]
        
        for milestone in milestones:
            if current_streak < milestone["days"]:
                return milestone
                
        return {"days": 365, "name": "Year of Growth", "reward": "Legendary Status"}
    
    def _get_streak_achievements(self, progress) -> List[Dict]:
        """Get unlocked streak achievements"""
        streak_achs = []
        
        if "streak_7" in progress.achievements:
            streak_achs.append({"id": "streak_7", "name": "Week Warrior", "icon": "🔥"})
        if "streak_30" in progress.achievements:
            streak_achs.append({"id": "streak_30", "name": "Monthly Master", "icon": "⚡"})
        if "streak_100" in progress.achievements:
            streak_achs.append({"id": "streak_100", "name": "Century Club", "icon": "💯"})
            
        return streak_achs


# Register agent
AgentRegistry.register(DailyCheckInAgent())
