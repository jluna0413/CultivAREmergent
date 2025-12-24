"""
CultivAR Gamification Engine

Features:
- XP/Level progression system
- Achievement badges
- Daily check-in streaks
- Community challenges
- NFT-gated rewards
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class AchievementCategory(Enum):
    """Achievement categories aligned with user journey"""
    DISCOVERY = "discovery"      # Finding new strains, breeders
    GROWING = "growing"          # Plant care milestones
    HARVEST = "harvest"          # Successful harvests
    COMMUNITY = "community"      # Social engagement
    LEARNING = "learning"        # Knowledge quests
    STREAKS = "streaks"          # Consistency rewards


@dataclass
class Achievement:
    """Achievement/badge definition"""
    id: str
    name: str
    description: str
    category: AchievementCategory
    xp_reward: int
    icon: str
    nft_unlock: Optional[str] = None  # NFT collection unlocked
    requirement: Dict[str, Any] = field(default_factory=dict)
    is_secret: bool = False


@dataclass
class UserProgress:
    """User's gamification progress"""
    user_id: int
    total_xp: int = 0
    level: int = 1
    current_streak: int = 0
    longest_streak: int = 0
    last_checkin: Optional[datetime] = None
    achievements: List[str] = field(default_factory=list)
    challenge_progress: Dict[str, int] = field(default_factory=dict)
    
    @property
    def xp_for_next_level(self) -> int:
        """XP needed for next level (exponential curve)"""
        return int(100 * (1.5 ** (self.level - 1)))
    
    @property
    def xp_in_current_level(self) -> int:
        """XP accumulated in current level"""
        total_for_level = sum(
            int(100 * (1.5 ** (l - 1))) 
            for l in range(1, self.level)
        )
        return self.total_xp - total_for_level
    
    @property
    def level_progress_percent(self) -> float:
        """Progress to next level as percentage"""
        return (self.xp_in_current_level / self.xp_for_next_level) * 100


# Pre-defined achievements
ACHIEVEMENTS = {
    # Discovery achievements
    "first_strain_view": Achievement(
        id="first_strain_view",
        name="Curious Cultivator",
        description="View your first strain in the marketplace",
        category=AchievementCategory.DISCOVERY,
        xp_reward=10,
        icon="🔍",
    ),
    "strain_collector_10": Achievement(
        id="strain_collector_10",
        name="Strain Collector",
        description="Add 10 strains to your collection",
        category=AchievementCategory.DISCOVERY,
        xp_reward=100,
        icon="🧬",
        requirement={"strains_collected": 10},
    ),
    "rare_genetics": Achievement(
        id="rare_genetics",
        name="Rare Genetics Hunter",
        description="Acquire a rare or limited edition strain",
        category=AchievementCategory.DISCOVERY,
        xp_reward=250,
        icon="💎",
        nft_unlock="rare_genetics_badge",
    ),
    
    # Growing achievements
    "first_plant": Achievement(
        id="first_plant",
        name="Green Thumb Initiate",
        description="Add your first plant",
        category=AchievementCategory.GROWING,
        xp_reward=25,
        icon="🌱",
    ),
    "plant_milestone_10": Achievement(
        id="plant_milestone_10",
        name="Garden Keeper",
        description="Successfully grow 10 plants",
        category=AchievementCategory.GROWING,
        xp_reward=200,
        icon="🌿",
        requirement={"plants_grown": 10},
    ),
    "perfect_environment": Achievement(
        id="perfect_environment",
        name="Climate Controller",
        description="Maintain optimal VPD for 7 consecutive days",
        category=AchievementCategory.GROWING,
        xp_reward=150,
        icon="🌡️",
        requirement={"optimal_vpd_days": 7},
    ),
    "ai_health_check": Achievement(
        id="ai_health_check",
        name="AI Diagnostician",
        description="Use AI plant health analysis 5 times",
        category=AchievementCategory.GROWING,
        xp_reward=75,
        icon="🤖",
        requirement={"ai_health_checks": 5},
    ),
    
    # Harvest achievements
    "first_harvest": Achievement(
        id="first_harvest",
        name="First Harvest",
        description="Complete your first successful harvest",
        category=AchievementCategory.HARVEST,
        xp_reward=100,
        icon="🌾",
        nft_unlock="first_harvest_nft",
    ),
    "yield_master": Achievement(
        id="yield_master",
        name="Yield Master",
        description="Exceed predicted yield by 20%",
        category=AchievementCategory.HARVEST,
        xp_reward=300,
        icon="📈",
    ),
    "cure_perfectionist": Achievement(
        id="cure_perfectionist",
        name="Cure Perfectionist",
        description="Complete a 30-day cure with optimal humidity",
        category=AchievementCategory.HARVEST,
        xp_reward=200,
        icon="🏺",
    ),
    
    # Streak achievements
    "streak_7": Achievement(
        id="streak_7",
        name="Week Warrior",
        description="7-day check-in streak",
        category=AchievementCategory.STREAKS,
        xp_reward=50,
        icon="🔥",
    ),
    "streak_30": Achievement(
        id="streak_30",
        name="Monthly Master",
        description="30-day check-in streak",
        category=AchievementCategory.STREAKS,
        xp_reward=200,
        icon="⚡",
        nft_unlock="dedication_badge",
    ),
    "streak_100": Achievement(
        id="streak_100",
        name="Century Club",
        description="100-day check-in streak",
        category=AchievementCategory.STREAKS,
        xp_reward=1000,
        icon="💯",
        nft_unlock="century_club_exclusive",
        is_secret=True,
    ),
    
    # Community achievements
    "first_share": Achievement(
        id="first_share",
        name="Community Contributor",
        description="Share your first grow journal entry",
        category=AchievementCategory.COMMUNITY,
        xp_reward=50,
        icon="📢",
    ),
    "helpful_grower": Achievement(
        id="helpful_grower",
        name="Helpful Grower",
        description="Receive 10 helpful votes on your advice",
        category=AchievementCategory.COMMUNITY,
        xp_reward=150,
        icon="🤝",
    ),
    
    # Learning achievements
    "knowledge_seeker": Achievement(
        id="knowledge_seeker",
        name="Knowledge Seeker",
        description="Complete 5 learning quests",
        category=AchievementCategory.LEARNING,
        xp_reward=100,
        icon="📚",
        requirement={"quests_completed": 5},
    ),
}


# Level benefits mapping
LEVEL_BENEFITS = {
    1: {"description": "Basic marketplace access", "discount": 0},
    5: {"description": "Early access notifications", "discount": 0},
    10: {"description": "5% marketplace discount", "discount": 5},
    15: {"description": "10% marketplace discount", "discount": 10},
    20: {"description": "15% marketplace discount + exclusive drops", "discount": 15},
    25: {"description": "VIP breeder access", "discount": 15},
    30: {"description": "NFT airdrops + premium features", "discount": 20},
}


class GamificationEngine:
    """
    Central gamification engine for CultivAR.
    
    Integrates with:
    - Agent system (XP rewards from agent interactions)
    - NFT marketplace (achievement-gated access)
    - Daily check-in (streak tracking)
    """
    
    def __init__(self):
        self.achievements = ACHIEVEMENTS
        self._user_progress: Dict[int, UserProgress] = {}
        
    def get_user_progress(self, user_id: int) -> UserProgress:
        """Get or create user progress"""
        if user_id not in self._user_progress:
            self._user_progress[user_id] = UserProgress(user_id=user_id)
        return self._user_progress[user_id]
    
    def award_xp(
        self, 
        user_id: int, 
        amount: int, 
        source: str,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Award XP to a user.
        
        Returns level-up info if applicable.
        """
        progress = self.get_user_progress(user_id)
        old_level = progress.level
        
        progress.total_xp += amount
        
        # Check for level up
        while progress.xp_in_current_level >= progress.xp_for_next_level:
            progress.level += 1
            
        result = {
            "xp_awarded": amount,
            "total_xp": progress.total_xp,
            "level": progress.level,
            "level_progress": progress.level_progress_percent,
            "source": source,
        }
        
        if progress.level > old_level:
            result["level_up"] = True
            result["new_level"] = progress.level
            result["new_benefits"] = self._get_level_benefits(progress.level)
            logger.info(f"User {user_id} leveled up to {progress.level}!")
            
        return result
    
    def daily_checkin(self, user_id: int) -> Dict[str, Any]:
        """
        Process daily check-in.
        
        Awards XP and tracks streaks.
        """
        progress = self.get_user_progress(user_id)
        now = datetime.utcnow()
        
        # Check if already checked in today
        if progress.last_checkin:
            if progress.last_checkin.date() == now.date():
                return {"already_checked_in": True, "streak": progress.current_streak}
                
            # Check if streak continues (checked in yesterday)
            yesterday = now.date() - timedelta(days=1)
            if progress.last_checkin.date() == yesterday:
                progress.current_streak += 1
            else:
                # Streak broken
                progress.current_streak = 1
        else:
            progress.current_streak = 1
            
        progress.last_checkin = now
        progress.longest_streak = max(progress.longest_streak, progress.current_streak)
        
        # Calculate XP bonus based on streak
        base_xp = 10
        streak_bonus = min(progress.current_streak * 2, 50)  # Cap at 50 bonus
        total_xp = base_xp + streak_bonus
        
        xp_result = self.award_xp(user_id, total_xp, "daily_checkin")
        
        # Check streak achievements
        streak_achievements = self._check_streak_achievements(progress)
        
        return {
            "checkin_successful": True,
            "current_streak": progress.current_streak,
            "longest_streak": progress.longest_streak,
            "xp_earned": total_xp,
            "streak_bonus": streak_bonus,
            "achievements_unlocked": streak_achievements,
            **xp_result,
        }
    
    def unlock_achievement(
        self, 
        user_id: int, 
        achievement_id: str
    ) -> Optional[Dict[str, Any]]:
        """Unlock an achievement for a user"""
        if achievement_id not in self.achievements:
            logger.warning(f"Unknown achievement: {achievement_id}")
            return None
            
        progress = self.get_user_progress(user_id)
        
        # Already unlocked
        if achievement_id in progress.achievements:
            return None
            
        achievement = self.achievements[achievement_id]
        progress.achievements.append(achievement_id)
        
        # Award XP
        xp_result = self.award_xp(
            user_id, 
            achievement.xp_reward, 
            f"achievement:{achievement_id}"
        )
        
        result = {
            "achievement_unlocked": True,
            "achievement": {
                "id": achievement.id,
                "name": achievement.name,
                "description": achievement.description,
                "icon": achievement.icon,
                "xp_reward": achievement.xp_reward,
                "nft_unlock": achievement.nft_unlock,
            },
            **xp_result,
        }
        
        logger.info(f"User {user_id} unlocked achievement: {achievement.name}")
        return result
    
    def check_achievements(
        self, 
        user_id: int, 
        metrics: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Check if user qualifies for any achievements based on metrics.
        
        Metrics example:
        {
            "plants_grown": 12,
            "strains_collected": 5,
            "ai_health_checks": 3,
        }
        """
        unlocked = []
        progress = self.get_user_progress(user_id)
        
        for ach_id, achievement in self.achievements.items():
            # Skip already unlocked
            if ach_id in progress.achievements:
                continue
                
            # Check requirements
            if achievement.requirement:
                meets_requirements = all(
                    metrics.get(key, 0) >= value 
                    for key, value in achievement.requirement.items()
                )
                if meets_requirements:
                    result = self.unlock_achievement(user_id, ach_id)
                    if result:
                        unlocked.append(result)
                        
        return unlocked
    
    def get_user_discount(self, user_id: int) -> int:
        """Get user's current marketplace discount percentage"""
        progress = self.get_user_progress(user_id)
        
        # Find highest applicable discount
        discount = 0
        for level, benefits in LEVEL_BENEFITS.items():
            if progress.level >= level:
                discount = max(discount, benefits.get("discount", 0))
                
        return discount
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get XP leaderboard"""
        sorted_users = sorted(
            self._user_progress.values(),
            key=lambda p: p.total_xp,
            reverse=True
        )[:limit]
        
        return [
            {
                "rank": i + 1,
                "user_id": p.user_id,
                "level": p.level,
                "total_xp": p.total_xp,
                "achievements_count": len(p.achievements),
            }
            for i, p in enumerate(sorted_users)
        ]
    
    def _check_streak_achievements(self, progress: UserProgress) -> List[str]:
        """Check and unlock streak-based achievements"""
        unlocked = []
        streak = progress.current_streak
        
        if streak >= 7 and "streak_7" not in progress.achievements:
            result = self.unlock_achievement(progress.user_id, "streak_7")
            if result:
                unlocked.append("streak_7")
                
        if streak >= 30 and "streak_30" not in progress.achievements:
            result = self.unlock_achievement(progress.user_id, "streak_30")
            if result:
                unlocked.append("streak_30")
                
        if streak >= 100 and "streak_100" not in progress.achievements:
            result = self.unlock_achievement(progress.user_id, "streak_100")
            if result:
                unlocked.append("streak_100")
                
        return unlocked
    
    def _get_level_benefits(self, level: int) -> Dict[str, Any]:
        """Get benefits for a specific level"""
        benefits = {"level": level, "perks": []}
        
        for lvl, benefit in LEVEL_BENEFITS.items():
            if level >= lvl:
                benefits["perks"].append(benefit["description"])
                benefits["discount"] = benefit.get("discount", 0)
                
        return benefits


# Singleton instance
gamification_engine = GamificationEngine()
