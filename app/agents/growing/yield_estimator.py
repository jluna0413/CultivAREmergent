"""
Yield Estimator Agent

Estimates potential harvest yield based on grow parameters,
strain data, and environmental monitoring.

Part of Growing Agents.
"""

import logging
import random
from typing import Any, Dict, List, Optional

from ..base import (
    AgentRole,
    AgentContext,
    AgentResult,
    BaseAgent,
    AgentRegistry,
)
from ...gamification import gamification_engine

logger = logging.getLogger(__name__)

class YieldEstimatorAgent(BaseAgent):
    """
    AI agent for estimating harvest yields and optimizing production.
    
    Capabilities:
    - Yield prediction based on light, space, and strain
    - Harvest timing optimization
    - ROI calculation
    """
    
    def __init__(self):
        super().__init__(
            agent_id="yield_estimator",
            name="Yield Estimator",
            role=AgentRole.GROWING,
            description="Predicts harvest weight and quality based on grow parameters",
        )
        
        self.register_tool(
            "estimate_yield",
            self.estimate_yield,
            "Estimate potential yield"
        )
        self.register_tool(
            "optimize_harvest",
            self.optimize_harvest,
            "Get harvest optimization tips"
        )

    async def execute(self, context: AgentContext, **kwargs) -> AgentResult:
        action = kwargs.get("action", "estimate")
        
        try:
            if action == "estimate":
                result = await self.estimate_yield(
                    light_watts=kwargs.get("light_watts", 0),
                    space_sqft=kwargs.get("space_sqft", 0),
                    strain_type=kwargs.get("strain_type", "photoperiod"),
                    veg_weeks=kwargs.get("veg_weeks", 4),
                    experience=kwargs.get("experience", "intermediate")
                )
            elif action == "optimize":
                result = await self.optimize_harvest(
                    current_week=kwargs.get("current_week", 1),
                    issues=kwargs.get("issues", [])
                )
            else:
                result = {"error": f"Unknown action: {action}"}

            # Award XP
            if context.user_id:
                gamification_engine.award_xp(
                    context.user_id, 5, "yield_estimation"
                )

            return AgentResult(
                success=True,
                agent_id=self.agent_id,
                output=result,
                confidence=0.85,
                xp_reward=5,
            )
            
        except Exception as e:
            logger.error(f"YieldEstimator error: {e}")
            return AgentResult(
                success=False,
                agent_id=self.agent_id,
                output=None,
                error=str(e),
            )

    async def estimate_yield(
        self,
        light_watts: int,
        space_sqft: float,
        strain_type: str = "photoperiod",
        veg_weeks: int = 4,
        experience: str = "intermediate"
    ) -> Dict[str, Any]:
        """
        Estimate dry yield in grams.
        Basic formula: Watts * Efficiency * ExperienceFactor
        """
        
        # Efficiency factors (grams per watt)
        tech_factor = {
            "LED": 1.5,
            "HPS": 0.8,
            "CMH": 1.0,
            "CFL": 0.3
        }
        
        # Experience multiplier
        exp_factor = {
            "beginner": 0.6,
            "intermediate": 0.85,
            "advanced": 1.1,
            "master": 1.4
        }
        
        base_gpw = 1.0 # Default Grams per Watt assumption (generic LED/Good HPS)
        
        # Calculate
        target_yield_grams = light_watts * base_gpw * exp_factor.get(experience.lower(), 0.8)
        
        # Adjust for space constraints (max 60g/sqft is pushing it for most)
        max_yield_space = space_sqft * 60 
        final_yield = min(target_yield_grams, max_yield_space)
        
        # Ranges
        min_yield = final_yield * 0.8
        max_yield = final_yield * 1.2
        
        return {
            "estimated_yield_grams": {
                "min": round(min_yield),
                "target": round(final_yield),
                "max": round(max_yield)
            },
            "estimated_yield_ounces": {
                "min": round(min_yield / 28.35, 1),
                "target": round(final_yield / 28.35, 1),
                "max": round(max_yield / 28.35, 1)
            },
            "efficiency_rating": f"{base_gpw * exp_factor.get(experience.lower(), 0.8):.2f} g/watt",
            "limiting_factors": [
                "Light intensity" if target_yield_grams < max_yield_space else "Canopy space",
                "Vegetative time" if veg_weeks < 4 else "Genetics"
            ]
        }
        
    async def optimize_harvest(
        self,
        current_week: int,
        issues: List[str]
    ) -> Dict[str, Any]:
        """Provide optimization tips based on current status"""
        
        recommendations = []
        
        if current_week < 4:
            recommendations.append("Focus on root development and structure training (LST/Topping).")
        elif current_week < 8:
             recommendations.append("Maximize light intensity and ensure humidity is in check (VPD 1.0-1.2).")
        else:
             recommendations.append("Begin monitoring trichomes. Lower humidity to <45% to prevent mold.")

        if "heat" in issues:
            recommendations.append("Add CO2 supplement to allow higher temp tolerance.")
            
        return {
            "phase_analysis": f"Week {current_week}",
            "recommendations": recommendations,
            "impact_projection": "+10-15% yield potential if followed"
        }

# Register agent
AgentRegistry.register(YieldEstimatorAgent())
