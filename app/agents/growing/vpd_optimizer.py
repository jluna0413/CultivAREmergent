"""
VPD Optimizer Agent

Real-time VPD monitoring and optimization recommendations.
Integrates with existing sensor infrastructure.

Part of Growing Agents.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import logging
import math

from ..base import (
    AgentRole,
    AgentContext,
    AgentResult,
    BaseAgent,
    AgentRegistry,
)
from ...gamification import gamification_engine

logger = logging.getLogger(__name__)


class GrowthStage(Enum):
    """Plant growth stages with optimal VPD ranges"""
    SEEDLING = "seedling"
    EARLY_VEG = "early_veg"
    LATE_VEG = "late_veg"
    EARLY_FLOWER = "early_flower"
    MID_FLOWER = "mid_flower"
    LATE_FLOWER = "late_flower"
    RIPENING = "ripening"


# Optimal VPD ranges by growth stage (in kPa)
VPD_OPTIMAL_RANGES = {
    GrowthStage.SEEDLING: (0.4, 0.8),
    GrowthStage.EARLY_VEG: (0.8, 1.0),
    GrowthStage.LATE_VEG: (1.0, 1.2),
    GrowthStage.EARLY_FLOWER: (1.0, 1.3),
    GrowthStage.MID_FLOWER: (1.2, 1.5),
    GrowthStage.LATE_FLOWER: (1.4, 1.6),
    GrowthStage.RIPENING: (1.4, 1.8),
}


@dataclass
class VPDReading:
    """VPD calculation result"""
    vpd: float
    temperature: float
    humidity: float
    leaf_temp: float
    timestamp: datetime
    is_optimal: bool
    stage: GrowthStage
    optimal_range: Tuple[float, float]
    deviation: float  # How far from optimal


@dataclass
class VPDRecommendation:
    """Recommendation to adjust environment"""
    action: str
    target_value: float
    current_value: float
    change_needed: float
    priority: str  # low, medium, high
    explanation: str


class VPDOptimizerAgent(BaseAgent):
    """
    VPD monitoring and optimization agent.
    
    Capabilities:
    - Calculate real-time VPD from sensor data
    - Provide stage-specific optimal ranges
    - Generate environment adjustment recommendations
    - Track VPD history and trends
    - Alert when VPD is out of range
    
    Integrates with:
    - Sensor infrastructure (temperature, humidity sensors)
    - Gamification (XP for maintaining optimal VPD)
    """
    
    def __init__(self):
        super().__init__(
            agent_id="vpd_optimizer",
            name="VPD Optimizer",
            role=AgentRole.GROWING,
            description="Real-time VPD monitoring and optimization",
        )
        
        # Register MCP tools
        self.register_tool(
            "calculate_vpd",
            self.calculate_vpd,
            "Calculate VPD from temperature and humidity"
        )
        self.register_tool(
            "get_vpd_recommendation",
            self.get_vpd_recommendation,
            "Get environment adjustment recommendations"
        )
        self.register_tool(
            "get_optimal_range",
            self.get_optimal_range,
            "Get optimal VPD range for growth stage"
        )
        self.register_tool(
            "analyze_vpd_trend",
            self.analyze_vpd_trend,
            "Analyze VPD trend over time"
        )
        
    async def execute(self, context: AgentContext, **kwargs) -> AgentResult:
        """Execute VPD optimization"""
        action = kwargs.get("action", "calculate")
        
        try:
            if action == "calculate":
                result = await self.calculate_vpd(
                    temperature=kwargs.get("temperature", 75.0),
                    humidity=kwargs.get("humidity", 55.0),
                    growth_stage=kwargs.get("growth_stage", "late_veg"),
                    leaf_temp_offset=kwargs.get("leaf_temp_offset", -2.0),
                )
            elif action == "recommend":
                result = await self.get_vpd_recommendation(
                    current_vpd=kwargs.get("current_vpd"),
                    temperature=kwargs.get("temperature"),
                    humidity=kwargs.get("humidity"),
                    growth_stage=kwargs.get("growth_stage", "late_veg"),
                )
            elif action == "optimal_range":
                result = await self.get_optimal_range(
                    growth_stage=kwargs.get("growth_stage", "late_veg"),
                )
            else:
                result = {"error": f"Unknown action: {action}"}
                
            # Award XP for using VPD optimizer
            if context.user_id:
                gamification_engine.award_xp(
                    context.user_id, 5, "vpd_optimization"
                )
                
            return AgentResult(
                success=True,
                agent_id=self.agent_id,
                output=result,
                confidence=0.95,
                xp_reward=5,
                next_actions=self._suggest_next_actions(result),
            )
            
        except Exception as e:
            logger.error(f"VPDOptimizer error: {e}")
            return AgentResult(
                success=False,
                agent_id=self.agent_id,
                output=None,
                error=str(e),
            )
    
    async def calculate_vpd(
        self,
        temperature: float,
        humidity: float,
        growth_stage: str = "late_veg",
        leaf_temp_offset: float = -2.0,
    ) -> Dict[str, Any]:
        """
        Calculate VPD from current sensor readings.
        
        Uses the standard VPD formula:
        VPD = SVP_leaf - AVP_air
        
        Where:
        - SVP = Saturation Vapor Pressure
        - AVP = Actual Vapor Pressure
        """
        # Convert stage string to enum
        try:
            stage = GrowthStage(growth_stage.lower())
        except ValueError:
            stage = GrowthStage.LATE_VEG
            
        # Calculate temps in Celsius
        air_temp_c = (temperature - 32) * 5.0 / 9.0
        leaf_temp_c = air_temp_c + (leaf_temp_offset * 5.0 / 9.0)
        
        # Calculate SVP at air and leaf temperatures
        # Formula: 0.61078 * exp(17.27 * T / (T + 237.3))
        svp_air = 0.61078 * math.exp((17.27 * air_temp_c) / (air_temp_c + 237.3))
        svp_leaf = 0.61078 * math.exp((17.27 * leaf_temp_c) / (leaf_temp_c + 237.3))
        
        # Calculate Actual Vapor Pressure
        avp = svp_air * (humidity / 100.0)
        
        # Calculate VPD
        vpd = max(0.0, round(svp_leaf - avp, 2))
        
        # Get optimal range for stage
        optimal_range = VPD_OPTIMAL_RANGES.get(stage, (1.0, 1.2))
        
        # Determine if optimal
        is_optimal = optimal_range[0] <= vpd <= optimal_range[1]
        
        # Calculate deviation from optimal
        if vpd < optimal_range[0]:
            deviation = optimal_range[0] - vpd
            status = "too_low"
        elif vpd > optimal_range[1]:
            deviation = vpd - optimal_range[1]
            status = "too_high"
        else:
            deviation = 0.0
            status = "optimal"
            
        # Get zone rating
        zone = self._get_vpd_zone(vpd, stage)
        
        return {
            "vpd": vpd,
            "vpd_formatted": f"{vpd} kPa",
            "temperature": temperature,
            "humidity": humidity,
            "leaf_temperature": round(temperature + leaf_temp_offset, 1),
            "growth_stage": stage.value,
            "optimal_range": {
                "min": optimal_range[0],
                "max": optimal_range[1],
            },
            "is_optimal": is_optimal,
            "status": status,
            "deviation": round(deviation, 2),
            "zone": zone,
            "timestamp": datetime.utcnow().isoformat(),
        }
    
    async def get_vpd_recommendation(
        self,
        current_vpd: Optional[float] = None,
        temperature: Optional[float] = None,
        humidity: Optional[float] = None,
        growth_stage: str = "late_veg",
    ) -> Dict[str, Any]:
        """
        Get recommendations to optimize VPD.
        
        Provides actionable adjustments for temperature and/or humidity.
        """
        # Calculate current VPD if not provided
        if current_vpd is None and temperature and humidity:
            calc_result = await self.calculate_vpd(
                temperature=temperature,
                humidity=humidity,
                growth_stage=growth_stage,
            )
            current_vpd = calc_result["vpd"]
            
        if current_vpd is None:
            return {"error": "VPD or temperature/humidity required"}
            
        # Get stage
        try:
            stage = GrowthStage(growth_stage.lower())
        except ValueError:
            stage = GrowthStage.LATE_VEG
            
        optimal_range = VPD_OPTIMAL_RANGES.get(stage, (1.0, 1.2))
        target_vpd = (optimal_range[0] + optimal_range[1]) / 2
        
        recommendations = []
        
        if current_vpd < optimal_range[0]:
            # VPD too low - need to increase
            # Options: Raise temp OR lower humidity
            
            if temperature and humidity:
                # Calculate target humidity to reach optimal VPD
                temp_c = (temperature - 32) * 5.0 / 9.0
                svp = 0.61078 * math.exp((17.27 * temp_c) / (temp_c + 237.3))
                target_avp = svp - target_vpd
                target_humidity = max(30, min(80, (target_avp / svp) * 100))
                
                humidity_change = humidity - target_humidity
                
                recommendations.append({
                    "action": "decrease_humidity",
                    "parameter": "humidity",
                    "current_value": humidity,
                    "target_value": round(target_humidity, 1),
                    "change_needed": round(humidity_change, 1),
                    "unit": "%",
                    "priority": "high" if current_vpd < optimal_range[0] - 0.3 else "medium",
                    "explanation": f"Lower humidity by {abs(humidity_change):.0f}% to increase VPD",
                    "methods": [
                        "Increase exhaust fan speed",
                        "Run dehumidifier",
                        "Improve air circulation",
                    ],
                })
                
                # Alternative: raise temperature
                recommendations.append({
                    "action": "increase_temperature",
                    "parameter": "temperature",
                    "current_value": temperature,
                    "target_value": round(temperature + 3, 1),
                    "change_needed": 3,
                    "unit": "°F",
                    "priority": "medium",
                    "explanation": "Alternatively, raise temperature by 3°F",
                    "methods": [
                        "Reduce AC/cooling",
                        "Add supplemental heating",
                        "Lower exhaust fan speed",
                    ],
                })
                
        elif current_vpd > optimal_range[1]:
            # VPD too high - need to decrease
            # Options: Lower temp OR raise humidity
            
            if temperature and humidity:
                temp_c = (temperature - 32) * 5.0 / 9.0
                svp = 0.61078 * math.exp((17.27 * temp_c) / (temp_c + 237.3))
                target_avp = svp - target_vpd
                target_humidity = max(30, min(80, (target_avp / svp) * 100))
                
                humidity_change = target_humidity - humidity
                
                recommendations.append({
                    "action": "increase_humidity",
                    "parameter": "humidity",
                    "current_value": humidity,
                    "target_value": round(target_humidity, 1),
                    "change_needed": round(humidity_change, 1),
                    "unit": "%",
                    "priority": "high" if current_vpd > optimal_range[1] + 0.3 else "medium",
                    "explanation": f"Raise humidity by {humidity_change:.0f}% to lower VPD",
                    "methods": [
                        "Run humidifier",
                        "Mist plants (lights off)",
                        "Add wet towels",
                    ],
                })
                
                recommendations.append({
                    "action": "decrease_temperature",
                    "parameter": "temperature",
                    "current_value": temperature,
                    "target_value": round(temperature - 3, 1),
                    "change_needed": -3,
                    "unit": "°F",
                    "priority": "medium",
                    "explanation": "Alternatively, lower temperature by 3°F",
                    "methods": [
                        "Increase AC/cooling",
                        "Increase exhaust fan speed",
                        "Check for heat sources",
                    ],
                })
        else:
            recommendations.append({
                "action": "maintain",
                "priority": "low",
                "explanation": f"VPD is optimal at {current_vpd} kPa. Maintain current conditions.",
            })
            
        return {
            "current_vpd": current_vpd,
            "target_vpd": target_vpd,
            "optimal_range": {
                "min": optimal_range[0],
                "max": optimal_range[1],
            },
            "growth_stage": stage.value,
            "recommendations": recommendations,
            "summary": self._generate_summary(current_vpd, optimal_range, recommendations),
        }
    
    async def get_optimal_range(self, growth_stage: str) -> Dict[str, Any]:
        """Get optimal VPD range for a growth stage"""
        try:
            stage = GrowthStage(growth_stage.lower())
        except ValueError:
            stage = GrowthStage.LATE_VEG
            
        optimal_range = VPD_OPTIMAL_RANGES.get(stage, (1.0, 1.2))
        
        # Get all stages for reference
        all_ranges = {
            s.value: {
                "min": r[0],
                "max": r[1],
                "average": round((r[0] + r[1]) / 2, 2),
            }
            for s, r in VPD_OPTIMAL_RANGES.items()
        }
        
        return {
            "growth_stage": stage.value,
            "optimal_range": {
                "min": optimal_range[0],
                "max": optimal_range[1],
                "average": round((optimal_range[0] + optimal_range[1]) / 2, 2),
            },
            "all_stages": all_ranges,
            "tips": self._get_stage_tips(stage),
        }
    
    async def analyze_vpd_trend(
        self,
        readings: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Analyze VPD trend over time"""
        if not readings:
            return {"error": "No readings provided"}
            
        vpd_values = [r.get("vpd", 0) for r in readings]
        
        avg_vpd = sum(vpd_values) / len(vpd_values)
        min_vpd = min(vpd_values)
        max_vpd = max(vpd_values)
        
        # Calculate trend
        if len(vpd_values) >= 2:
            first_half = vpd_values[:len(vpd_values)//2]
            second_half = vpd_values[len(vpd_values)//2:]
            trend = sum(second_half)/len(second_half) - sum(first_half)/len(first_half)
        else:
            trend = 0
            
        # Calculate stability (standard deviation)
        variance = sum((v - avg_vpd) ** 2 for v in vpd_values) / len(vpd_values)
        std_dev = variance ** 0.5
        
        stability = "stable" if std_dev < 0.15 else "moderate" if std_dev < 0.3 else "unstable"
        
        return {
            "period": {
                "readings_count": len(readings),
                "first": readings[0].get("timestamp") if readings else None,
                "last": readings[-1].get("timestamp") if readings else None,
            },
            "statistics": {
                "average": round(avg_vpd, 2),
                "min": round(min_vpd, 2),
                "max": round(max_vpd, 2),
                "range": round(max_vpd - min_vpd, 2),
                "std_dev": round(std_dev, 2),
            },
            "trend": {
                "direction": "increasing" if trend > 0.05 else "decreasing" if trend < -0.05 else "stable",
                "change": round(trend, 2),
            },
            "stability": stability,
            "assessment": self._assess_trend(avg_vpd, std_dev, stability),
        }
    
    def _get_vpd_zone(self, vpd: float, stage: GrowthStage) -> Dict[str, Any]:
        """Get VPD zone classification"""
        optimal = VPD_OPTIMAL_RANGES.get(stage, (1.0, 1.2))
        
        if vpd < 0.4:
            return {"name": "Danger Low", "color": "red", "risk": "high"}
        elif vpd < optimal[0]:
            return {"name": "Low", "color": "yellow", "risk": "medium"}
        elif vpd <= optimal[1]:
            return {"name": "Optimal", "color": "green", "risk": "none"}
        elif vpd <= 1.8:
            return {"name": "High", "color": "yellow", "risk": "medium"}
        else:
            return {"name": "Danger High", "color": "red", "risk": "high"}
    
    def _get_stage_tips(self, stage: GrowthStage) -> List[str]:
        """Get tips for managing VPD at growth stage"""
        tips = {
            GrowthStage.SEEDLING: [
                "Keep humidity high (70-80%) for seedlings",
                "Lower VPD prevents excessive transpiration",
                "Use a humidity dome if needed",
            ],
            GrowthStage.EARLY_VEG: [
                "Gradually lower humidity as roots develop",
                "Plants can handle slightly higher VPD now",
                "Monitor for wilting - sign of VPD too high",
            ],
            GrowthStage.LATE_VEG: [
                "VPD can be pushed higher to encourage growth",
                "Strong root system supports higher transpiration",
                "Good time to train plants for structure",
            ],
            GrowthStage.EARLY_FLOWER: [
                "Maintain stable VPD for stretch phase",
                "Avoid big swings that stress plants",
                "Higher VPD promotes resin production",
            ],
            GrowthStage.MID_FLOWER: [
                "VPD at higher end promotes terpene production",
                "Monitor for bud rot if humidity spikes",
                "Consider defoliation to improve airflow",
            ],
            GrowthStage.LATE_FLOWER: [
                "Keep VPD higher to prevent mold",
                "Lower humidity as buds fatten",
                "Watch for foxtailing from heat stress",
            ],
            GrowthStage.RIPENING: [
                "Highest VPD tolerance - push transpiration",
                "Dry conditions help with final ripening",
                "Can drop humidity below 40% if needed",
            ],
        }
        return tips.get(stage, ["Maintain VPD within optimal range"])
    
    def _generate_summary(
        self, 
        current_vpd: float, 
        optimal_range: Tuple[float, float],
        recommendations: List[Dict]
    ) -> str:
        """Generate human-readable summary"""
        if optimal_range[0] <= current_vpd <= optimal_range[1]:
            return f"✅ VPD is optimal at {current_vpd} kPa. Keep up the good work!"
        elif current_vpd < optimal_range[0]:
            diff = optimal_range[0] - current_vpd
            return f"⚠️ VPD is {diff:.2f} kPa below optimal. Consider lowering humidity or raising temperature."
        else:
            diff = current_vpd - optimal_range[1]
            return f"⚠️ VPD is {diff:.2f} kPa above optimal. Consider raising humidity or lowering temperature."
    
    def _assess_trend(self, avg_vpd: float, std_dev: float, stability: str) -> str:
        """Generate trend assessment"""
        if stability == "unstable":
            return "⚠️ VPD is fluctuating significantly. Check environmental controls and seal air leaks."
        elif std_dev < 0.1:
            return "✅ Excellent VPD stability. Environment is well controlled."
        else:
            return "👍 Good VPD consistency. Minor fluctuations are normal."
    
    def _suggest_next_actions(self, result: Dict) -> List[str]:
        """Suggest next actions based on result"""
        actions = ["log_reading"]
        
        if result.get("is_optimal") == False:
            actions.append("adjust_environment")
            actions.append("set_reminder")
            
        if result.get("zone", {}).get("risk") == "high":
            actions.append("alert_user")
            
        return actions


# Register agent
AgentRegistry.register(VPDOptimizerAgent())
