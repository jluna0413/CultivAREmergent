"""
Grow Buddy Agent

AI-powered grow companion that provides personalized guidance,
mentorship matching, and community connections.

Part of Community Agents.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum
import logging
import random

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


class ExperienceLevel(str, Enum):
    """Grower experience levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"
    MASTER = "master"


class GrowStyle(str, Enum):
    """Growing styles/methods"""
    SOIL_ORGANIC = "soil_organic"
    COCO_COIR = "coco_coir"
    HYDRO_DWC = "hydro_dwc"
    HYDRO_RDWC = "hydro_rdwc"
    AEROPONICS = "aeroponics"
    LIVING_SOIL = "living_soil"
    OUTDOOR = "outdoor"


class MentorProfile(BaseModel):
    """Community mentor profile"""
    user_id: int
    username: str
    experience_level: ExperienceLevel
    years_growing: int
    specialties: List[str]
    grow_styles: List[GrowStyle]
    rating: float = Field(ge=0, le=5)
    mentees_helped: int
    available: bool = True


class GrowBuddyAgent(BaseAgent):
    """
    AI grow companion and community connection agent.
    
    Capabilities:
    - Personalized growing advice
    - Mentor matching
    - Community Q&A
    - Grow journey milestones
    - Peer recommendations
    
    Integrates with:
    - User profiles
    - Gamification (XP for helping)
    - Community forums
    """
    
    def __init__(self):
        super().__init__(
            agent_id="grow_buddy",
            name="Grow Buddy",
            role=AgentRole.COMMUNITY,
            description="AI grow companion with mentorship and community connections",
        )
        
        # Register MCP tools
        self.register_tool(
            "get_advice",
            self.get_personalized_advice,
            "Get personalized growing advice"
        )
        self.register_tool(
            "find_mentor",
            self.find_mentor,
            "Find a mentor matching your needs"
        )
        self.register_tool(
            "get_milestones",
            self.get_grow_milestones,
            "Get grow journey milestones"
        )
        self.register_tool(
            "ask_community",
            self.ask_community,
            "Ask the community a question"
        )
        self.register_tool(
            "daily_tip",
            self.get_daily_tip,
            "Get daily growing tip"
        )
        
        # Mock mentor database
        self._mentors = self._load_mock_mentors()
        
    async def execute(self, context: AgentContext, **kwargs) -> AgentResult:
        """Execute grow buddy operation"""
        action = kwargs.get("action", "advice")
        
        try:
            if action == "advice":
                result = await self.get_personalized_advice(
                    topic=kwargs.get("topic", "general"),
                    experience_level=kwargs.get("experience_level", "beginner"),
                    grow_style=kwargs.get("grow_style"),
                    current_issue=kwargs.get("current_issue"),
                )
            elif action == "mentor":
                result = await self.find_mentor(
                    experience_level=kwargs.get("experience_level", "beginner"),
                    grow_style=kwargs.get("grow_style"),
                    specialty=kwargs.get("specialty"),
                )
            elif action == "milestones":
                result = await self.get_grow_milestones(
                    user_id=context.user_id,
                    current_phase=kwargs.get("current_phase", "seedling"),
                )
            elif action == "ask":
                result = await self.ask_community(
                    question=kwargs.get("question"),
                    category=kwargs.get("category", "general"),
                )
            elif action == "tip":
                result = await self.get_daily_tip(
                    experience_level=kwargs.get("experience_level", "beginner"),
                )
            else:
                result = {"error": f"Unknown action: {action}"}
                
            # Award XP for engagement
            if context.user_id:
                gamification_engine.award_xp(
                    context.user_id, 5, "grow_buddy_interaction"
                )
                
            return AgentResult(
                success=True,
                agent_id=self.agent_id,
                output=result,
                confidence=0.85,
                xp_reward=5,
                next_actions=["ask_followup", "find_mentor", "share_progress"],
            )
            
        except Exception as e:
            logger.error(f"GrowBuddy error: {e}")
            return AgentResult(
                success=False,
                agent_id=self.agent_id,
                output=None,
                error=str(e),
            )
    
    async def get_personalized_advice(
        self,
        topic: str = "general",
        experience_level: str = "beginner",
        grow_style: Optional[str] = None,
        current_issue: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get personalized growing advice"""
        
        # Topic-specific advice
        advice_library = {
            "watering": {
                "beginner": [
                    "Water when top inch of soil is dry",
                    "Lift pots to feel weight - light = needs water",
                    "Better to underwater than overwater",
                    "Use room temperature water",
                ],
                "intermediate": [
                    "Consider drip irrigation for consistency",
                    "Track runoff EC to monitor salt buildup",
                    "Adjust watering frequency based on plant size",
                ],
                "advanced": [
                    "Implement sensor-based automated watering",
                    "Use pulse irrigation for coco",
                    "Monitor VPD to predict water needs",
                ],
            },
            "nutrients": {
                "beginner": [
                    "Start with half-strength nutrients",
                    "Less is more - you can always add",
                    "Always pH your nutrient solution",
                    "Watch for tip burn - sign of overfeeding",
                ],
                "intermediate": [
                    "Learn to read your plants' needs",
                    "Supplement cal-mag in coco/hydro",
                    "Track EC in and out",
                ],
                "advanced": [
                    "Custom nutrient recipes per strain",
                    "Foliar feeding for quick corrections",
                    "Organic amendments for living soil",
                ],
            },
            "lighting": {
                "beginner": [
                    "18/6 for veg, 12/12 for flower",
                    "Keep proper distance from canopy",
                    "Dim lights for seedlings",
                ],
                "intermediate": [
                    "Consider DLI (Daily Light Integral)",
                    "Adjust intensity by growth stage",
                    "Supplement with side lighting",
                ],
                "advanced": [
                    "UV supplementation for terpenes",
                    "Far-red for stretch control",
                    "Custom light spectrums per phase",
                ],
            },
            "general": {
                "beginner": [
                    "Keep a grow journal - track everything",
                    "Start simple, master basics first",
                    "Don't overthink it - plants want to grow",
                    "Join the community and ask questions",
                ],
                "intermediate": [
                    "Experiment with training techniques",
                    "Dial in your environment first",
                    "Clone your best performers",
                ],
                "advanced": [
                    "Phenotype hunting for keepers",
                    "Environmental manipulation for quality",
                    "Share knowledge with the community",
                ],
            },
        }
        
        level = experience_level.lower()
        topic_advice = advice_library.get(topic.lower(), advice_library["general"])
        level_advice = topic_advice.get(level, topic_advice.get("beginner", []))
        
        response = {
            "topic": topic,
            "experience_level": level,
            "advice": level_advice,
            "pro_tip": random.choice(level_advice) if level_advice else "Keep learning!",
        }
        
        if current_issue:
            response["issue_addressed"] = current_issue
            response["specific_advice"] = f"For '{current_issue}': Start by checking your environment basics - VPD, pH, and light distance."
            
        if grow_style:
            response["style_note"] = f"These tips are adapted for {grow_style} growing."
            
        return response
    
    async def find_mentor(
        self,
        experience_level: str = "beginner",
        grow_style: Optional[str] = None,
        specialty: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Find a mentor matching user's needs"""
        
        # Filter mentors by criteria
        matches = []
        for mentor in self._mentors:
            score = 0
            reasons = []
            
            # Experience level match (mentor should be more experienced)
            level_order = ["beginner", "intermediate", "advanced", "expert", "master"]
            user_idx = level_order.index(experience_level.lower()) if experience_level.lower() in level_order else 0
            mentor_idx = level_order.index(mentor["experience_level"]) if mentor["experience_level"] in level_order else 0
            
            if mentor_idx > user_idx:
                score += 0.3
                reasons.append("More experienced")
                
            # Grow style match
            if grow_style and grow_style.lower() in [s.lower() for s in mentor.get("grow_styles", [])]:
                score += 0.3
                reasons.append(f"Experienced in {grow_style}")
                
            # Specialty match
            if specialty and specialty.lower() in [s.lower() for s in mentor.get("specialties", [])]:
                score += 0.3
                reasons.append(f"Specializes in {specialty}")
                
            # Availability
            if mentor.get("available", False):
                score += 0.1
                reasons.append("Currently available")
                
            if score > 0.2:
                matches.append({
                    **mentor,
                    "match_score": round(score, 2),
                    "match_reasons": reasons,
                })
                
        # Sort by score
        matches.sort(key=lambda x: x["match_score"], reverse=True)
        
        return {
            "search_criteria": {
                "experience_level": experience_level,
                "grow_style": grow_style,
                "specialty": specialty,
            },
            "total_matches": len(matches),
            "recommended_mentors": matches[:5],
            "how_to_connect": [
                "Send a mentor request through the app",
                "Join their open grow sessions",
                "Ask questions in their Discord",
            ],
        }
    
    async def get_grow_milestones(
        self,
        user_id: Optional[int],
        current_phase: str = "seedling",
    ) -> Dict[str, Any]:
        """Get grow journey milestones and achievements"""
        
        milestones = {
            "seedling": {
                "current": "🌱 Seedling Stage",
                "achievements": [
                    {"name": "First Sprout", "xp": 50, "unlocked": True},
                    {"name": "Healthy Cotyledons", "xp": 25, "unlocked": False},
                ],
                "next_milestone": "First True Leaves",
                "tips": ["Keep humidity high", "Gentle lighting", "Don't overwater"],
            },
            "veg": {
                "current": "🌿 Vegetative Stage",
                "achievements": [
                    {"name": "Veg Warrior", "xp": 100, "unlocked": False},
                    {"name": "Training Master", "xp": 75, "unlocked": False},
                    {"name": "Clone Creator", "xp": 150, "unlocked": False},
                ],
                "next_milestone": "Ready for Flower",
                "tips": ["Focus on structure", "Train for yield", "Build strong roots"],
            },
            "flower": {
                "current": "🌺 Flowering Stage",
                "achievements": [
                    {"name": "First Flowers", "xp": 100, "unlocked": False},
                    {"name": "Trichome Tracker", "xp": 75, "unlocked": False},
                    {"name": "Frost Factory", "xp": 200, "unlocked": False},
                ],
                "next_milestone": "Harvest Ready",
                "tips": ["Watch for deficiencies", "Manage humidity", "Be patient"],
            },
            "harvest": {
                "current": "✂️ Harvest Time",
                "achievements": [
                    {"name": "First Harvest", "xp": 500, "unlocked": False},
                    {"name": "Perfect Timing", "xp": 300, "unlocked": False},
                    {"name": "Yield Master", "xp": 250, "unlocked": False},
                ],
                "next_milestone": "Cure Complete",
                "tips": ["Check trichomes", "Prepare dry space", "Take photos!"],
            },
        }
        
        phase_data = milestones.get(current_phase.lower(), milestones["seedling"])
        
        return {
            "user_id": user_id,
            **phase_data,
            "overall_progress": {
                "grows_completed": 0,  # Would pull from user data
                "total_xp_earned": 0,
                "next_level": "Apprentice Grower",
            },
            "community_comparison": "You're doing great! Keep it up! 🌟",
        }
    
    async def ask_community(
        self,
        question: Optional[str],
        category: str = "general",
    ) -> Dict[str, Any]:
        """Post a question to the community"""
        if not question:
            return {"error": "Please provide a question"}
            
        # Mock community response simulation
        return {
            "question": question,
            "category": category,
            "posted": True,
            "estimated_response_time": "Usually within 1 hour",
            "similar_questions": [
                {"title": "How often should I water seedlings?", "answers": 12},
                {"title": "Best nutrients for coco?", "answers": 24},
            ],
            "helpful_resources": [
                "Check our FAQ section",
                "Watch the beginner tutorial series",
                "Join Discord for real-time help",
            ],
            "xp_earned": 5,
        }
    
    async def get_daily_tip(self, experience_level: str = "beginner") -> Dict[str, Any]:
        """Get daily growing tip"""
        
        tips = {
            "beginner": [
                "🌱 Tip: Check your plants at the same time each day to notice changes faster.",
                "💧 Tip: Let tap water sit 24 hours before using to dechlorinate.",
                "🌡️ Tip: Keep temps 75-85°F during lights on, drop 10° at night.",
                "📝 Tip: Take a photo every day - you'll love looking back!",
            ],
            "intermediate": [
                "🔬 Tip: Monitor runoff EC to catch salt buildup early.",
                "🌿 Tip: Defoliate strategically for better light penetration.",
                "🧪 Tip: Calibrate your pH meter monthly for accuracy.",
            ],
            "advanced": [
                "🧬 Tip: Track terpene profiles to identify keepers.",
                "🌡️ Tip: Experiment with temperature differentials for color.",
                "📊 Tip: Log environmental data to optimize future grows.",
            ],
        }
        
        level = experience_level.lower()
        level_tips = tips.get(level, tips["beginner"])
        daily_tip = random.choice(level_tips)
        
        return {
            "tip": daily_tip,
            "experience_level": level,
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "share": f"Share this tip with #GrowTip on social!",
            "xp_for_reading": 2,
        }
    
    def _load_mock_mentors(self) -> List[Dict]:
        """Load mock mentor database"""
        return [
            {
                "user_id": 1001,
                "username": "GrowMaster420",
                "experience_level": "master",
                "years_growing": 15,
                "specialties": ["training", "organic", "phenohunting"],
                "grow_styles": ["living_soil", "outdoor"],
                "rating": 4.9,
                "mentees_helped": 127,
                "available": True,
            },
            {
                "user_id": 1002,
                "username": "HydroQueen",
                "experience_level": "expert",
                "years_growing": 8,
                "specialties": ["hydro", "automation", "nutrients"],
                "grow_styles": ["hydro_dwc", "hydro_rdwc", "aeroponics"],
                "rating": 4.8,
                "mentees_helped": 89,
                "available": True,
            },
            {
                "user_id": 1003,
                "username": "CocoKing",
                "experience_level": "advanced",
                "years_growing": 5,
                "specialties": ["coco", "autoflowers", "leds"],
                "grow_styles": ["coco_coir"],
                "rating": 4.7,
                "mentees_helped": 45,
                "available": True,
            },
        ]


# Register agent
AgentRegistry.register(GrowBuddyAgent())
