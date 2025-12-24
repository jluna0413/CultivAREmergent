"""
Nutrient Advisor Agent

Stage-based feeding schedules and deficiency diagnosis.
Integrates with plant growth stages and sensor data.

Part of Growing Agents.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum
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


class GrowthPhase(Enum):
    """Growth phases for nutrient scheduling"""
    SEEDLING = "seedling"
    EARLY_VEG = "early_veg"
    LATE_VEG = "late_veg"
    TRANSITION = "transition"
    EARLY_FLOWER = "early_flower"
    MID_FLOWER = "mid_flower"
    LATE_FLOWER = "late_flower"
    FLUSH = "flush"


class MediumType(Enum):
    """Growing medium types"""
    SOIL = "soil"
    COCO = "coco"
    HYDRO = "hydro"
    DWC = "dwc"
    RDWC = "rdwc"


class NutrientElement(Enum):
    """Essential nutrient elements"""
    NITROGEN = "nitrogen"
    PHOSPHORUS = "phosphorus"
    POTASSIUM = "potassium"
    CALCIUM = "calcium"
    MAGNESIUM = "magnesium"
    SULFUR = "sulfur"
    IRON = "iron"
    MANGANESE = "manganese"
    ZINC = "zinc"
    BORON = "boron"


# EC/PPM ranges by growth phase
EC_RANGES = {
    GrowthPhase.SEEDLING: (0.4, 0.8),
    GrowthPhase.EARLY_VEG: (0.8, 1.2),
    GrowthPhase.LATE_VEG: (1.2, 1.6),
    GrowthPhase.TRANSITION: (1.4, 1.8),
    GrowthPhase.EARLY_FLOWER: (1.6, 2.0),
    GrowthPhase.MID_FLOWER: (1.8, 2.2),
    GrowthPhase.LATE_FLOWER: (1.6, 2.0),
    GrowthPhase.FLUSH: (0.0, 0.2),
}

# pH ranges by medium
PH_RANGES = {
    MediumType.SOIL: (6.0, 7.0),
    MediumType.COCO: (5.8, 6.2),
    MediumType.HYDRO: (5.5, 6.0),
    MediumType.DWC: (5.5, 6.0),
    MediumType.RDWC: (5.5, 6.0),
}

# NPK ratios by phase
NPK_RATIOS = {
    GrowthPhase.SEEDLING: {"N": 1, "P": 1, "K": 1},
    GrowthPhase.EARLY_VEG: {"N": 3, "P": 1, "K": 2},
    GrowthPhase.LATE_VEG: {"N": 3, "P": 1, "K": 2},
    GrowthPhase.TRANSITION: {"N": 2, "P": 2, "K": 2},
    GrowthPhase.EARLY_FLOWER: {"N": 1, "P": 3, "K": 2},
    GrowthPhase.MID_FLOWER: {"N": 1, "P": 3, "K": 3},
    GrowthPhase.LATE_FLOWER: {"N": 0, "P": 3, "K": 3},
    GrowthPhase.FLUSH: {"N": 0, "P": 0, "K": 0},
}


@dataclass
class DeficiencySymptom:
    """Symptom of nutrient deficiency"""
    element: NutrientElement
    symptoms: List[str]
    affected_leaves: str  # "old", "new", or "all"
    severity: str  # "mild", "moderate", "severe"
    solution: List[str]


# Common deficiency patterns
DEFICIENCY_PATTERNS = {
    NutrientElement.NITROGEN: {
        "symptoms": [
            "Yellowing of lower/older leaves",
            "Pale green overall color",
            "Stunted growth",
            "Early leaf drop",
        ],
        "affected_leaves": "old",
        "solutions": [
            "Increase nitrogen in feed",
            "Check pH - optimal 6.0-6.5 for N uptake",
            "Foliar spray with diluted nitrogen source",
        ],
    },
    NutrientElement.PHOSPHORUS: {
        "symptoms": [
            "Dark green or purple leaves",
            "Purple/red stems",
            "Slow growth",
            "Delayed flowering",
        ],
        "affected_leaves": "old",
        "solutions": [
            "Increase phosphorus",
            "Check temperature - cold inhibits P uptake",
            "Ensure pH is 6.0-7.0",
        ],
    },
    NutrientElement.POTASSIUM: {
        "symptoms": [
            "Brown/burnt leaf edges",
            "Curling leaf tips",
            "Weak stems",
            "Slow bud development",
        ],
        "affected_leaves": "old",
        "solutions": [
            "Increase potassium",
            "Check for salt buildup - flush if needed",
            "Ensure pH 6.0-7.0",
        ],
    },
    NutrientElement.CALCIUM: {
        "symptoms": [
            "Brown spots on new leaves",
            "Curled/distorted new growth",
            "Hollow stems",
            "Blossom end rot",
        ],
        "affected_leaves": "new",
        "solutions": [
            "Add Cal-Mag supplement",
            "Check pH - Ca locks out below 6.2",
            "Avoid excess potassium which blocks Ca",
        ],
    },
    NutrientElement.MAGNESIUM: {
        "symptoms": [
            "Interveinal yellowing",
            "Yellow between veins, veins stay green",
            "Leaf edges curl up",
            "Lower leaves affected first",
        ],
        "affected_leaves": "old",
        "solutions": [
            "Add Epsom salt (1 tsp/gallon)",
            "Add Cal-Mag supplement",
            "Ensure pH 6.0-7.0",
        ],
    },
    NutrientElement.IRON: {
        "symptoms": [
            "New leaves turn yellow",
            "Veins remain green (similar to Mg but on new growth)",
            "Bleached appearance",
        ],
        "affected_leaves": "new",
        "solutions": [
            "Lower pH to 5.5-6.5",
            "Add chelated iron supplement",
            "Check for calcium/phosphorus lockout",
        ],
    },
}


class NutrientAdvisorAgent(BaseAgent):
    """
    Nutrient management and deficiency diagnosis agent.
    
    Capabilities:
    - Stage-specific feeding schedules
    - EC/PPM and pH recommendations
    - Deficiency symptom analysis
    - Nutrient solution calculator
    - Flush timeline guidance
    
    Integrates with:
    - Plant data (growth stage, medium)
    - Sensor data (EC, pH if available)
    - Gamification (XP for consistent feeding)
    """
    
    def __init__(self):
        super().__init__(
            agent_id="nutrient_advisor",
            name="Nutrient Advisor",
            role=AgentRole.GROWING,
            description="Stage-based feeding schedules and deficiency diagnosis",
        )
        
        # Register MCP tools
        self.register_tool(
            "get_feeding_schedule",
            self.get_feeding_schedule,
            "Get feeding schedule for growth phase"
        )
        self.register_tool(
            "diagnose_deficiency",
            self.diagnose_deficiency,
            "Diagnose nutrient deficiency from symptoms"
        )
        self.register_tool(
            "calculate_solution",
            self.calculate_solution,
            "Calculate nutrient solution strength"
        )
        self.register_tool(
            "get_flush_schedule",
            self.get_flush_schedule,
            "Get pre-harvest flush schedule"
        )
        
    async def execute(self, context: AgentContext, **kwargs) -> AgentResult:
        """Execute nutrient advisory"""
        action = kwargs.get("action", "schedule")
        
        try:
            if action == "schedule":
                result = await self.get_feeding_schedule(
                    growth_phase=kwargs.get("growth_phase", "late_veg"),
                    medium=kwargs.get("medium", "coco"),
                    week_in_phase=kwargs.get("week_in_phase", 1),
                )
            elif action == "diagnose":
                result = await self.diagnose_deficiency(
                    symptoms=kwargs.get("symptoms", []),
                    affected_area=kwargs.get("affected_area", "lower_leaves"),
                )
            elif action == "calculate":
                result = await self.calculate_solution(
                    target_ec=kwargs.get("target_ec", 1.4),
                    water_volume_gallons=kwargs.get("water_volume", 5),
                    growth_phase=kwargs.get("growth_phase", "late_veg"),
                )
            elif action == "flush":
                result = await self.get_flush_schedule(
                    days_to_harvest=kwargs.get("days_to_harvest", 14),
                    medium=kwargs.get("medium", "coco"),
                )
            else:
                result = {"error": f"Unknown action: {action}"}
                
            # Award XP
            if context.user_id:
                gamification_engine.award_xp(
                    context.user_id, 5, "nutrient_advisory"
                )
                
            return AgentResult(
                success=True,
                agent_id=self.agent_id,
                output=result,
                confidence=0.9,
                xp_reward=5,
                next_actions=["log_feeding", "set_reminder"],
            )
            
        except Exception as e:
            logger.error(f"NutrientAdvisor error: {e}")
            return AgentResult(
                success=False,
                agent_id=self.agent_id,
                output=None,
                error=str(e),
            )
    
    async def get_feeding_schedule(
        self,
        growth_phase: str,
        medium: str = "coco",
        week_in_phase: int = 1,
    ) -> Dict[str, Any]:
        """
        Get feeding schedule for current growth phase.
        
        Provides EC/PPM targets, pH range, and NPK ratios.
        """
        try:
            phase = GrowthPhase(growth_phase.lower())
        except ValueError:
            phase = GrowthPhase.LATE_VEG
            
        try:
            med_type = MediumType(medium.lower())
        except ValueError:
            med_type = MediumType.COCO
            
        ec_range = EC_RANGES.get(phase, (1.2, 1.6))
        ph_range = PH_RANGES.get(med_type, (5.8, 6.2))
        npk_ratio = NPK_RATIOS.get(phase, {"N": 2, "P": 2, "K": 2})
        
        # Calculate PPM from EC (EC * 500 or EC * 700 scale)
        ppm_500 = (ec_range[0] * 500, ec_range[1] * 500)
        ppm_700 = (ec_range[0] * 700, ec_range[1] * 700)
        
        # Adjust for week in phase
        week_modifier = min(1.0 + (week_in_phase - 1) * 0.1, 1.3)  # Max 30% increase
        adjusted_ec = (
            round(ec_range[0] * week_modifier, 2),
            round(ec_range[1] * week_modifier, 2),
        )
        
        schedule = {
            "growth_phase": phase.value,
            "week_in_phase": week_in_phase,
            "medium": med_type.value,
            "ec_target": {
                "min": adjusted_ec[0],
                "max": adjusted_ec[1],
                "unit": "mS/cm",
            },
            "ppm_target_500_scale": {
                "min": int(adjusted_ec[0] * 500),
                "max": int(adjusted_ec[1] * 500),
            },
            "ppm_target_700_scale": {
                "min": int(adjusted_ec[0] * 700),
                "max": int(adjusted_ec[1] * 700),
            },
            "ph_range": {
                "min": ph_range[0],
                "max": ph_range[1],
                "optimal": round((ph_range[0] + ph_range[1]) / 2, 1),
            },
            "npk_ratio": npk_ratio,
            "feeding_frequency": self._get_feeding_frequency(phase, med_type),
            "additives": self._get_recommended_additives(phase),
            "tips": self._get_phase_tips(phase),
        }
        
        return schedule
    
    async def diagnose_deficiency(
        self,
        symptoms: List[str],
        affected_area: str = "lower_leaves",
    ) -> Dict[str, Any]:
        """
        Diagnose nutrient deficiency from symptoms.
        
        Uses symptom matching to identify likely deficiencies.
        """
        if not symptoms:
            return {
                "error": "No symptoms provided",
                "help": "Describe symptoms like: yellowing, brown spots, curling, etc.",
            }
            
        # Normalize symptoms
        symptoms_lower = [s.lower() for s in symptoms]
        affected_lower = affected_area.lower()
        
        # Score each potential deficiency
        matches = []
        
        for element, pattern in DEFICIENCY_PATTERNS.items():
            score = 0
            matched_symptoms = []
            
            # Check for matching symptoms
            for symptom in pattern["symptoms"]:
                symptom_words = symptom.lower().split()
                for user_symptom in symptoms_lower:
                    if any(word in user_symptom for word in symptom_words[:3]):
                        score += 1
                        matched_symptoms.append(symptom)
                        break
                        
            # Check affected area match
            if pattern["affected_leaves"] == "old" and "old" in affected_lower or "lower" in affected_lower:
                score += 2
            elif pattern["affected_leaves"] == "new" and "new" in affected_lower or "upper" in affected_lower:
                score += 2
                
            if score > 0:
                matches.append({
                    "element": element.value,
                    "confidence": min(score / 5, 1.0),  # Normalize to 0-1
                    "matched_symptoms": matched_symptoms,
                    "solutions": pattern["solutions"],
                    "affected_leaves": pattern["affected_leaves"],
                })
                
        # Sort by confidence
        matches.sort(key=lambda x: x["confidence"], reverse=True)
        
        if not matches:
            return {
                "diagnosis": "Unable to identify deficiency",
                "suggestion": "Check pH and EC levels first - most issues stem from pH lockout",
                "general_tips": [
                    "Flush medium with pH'd water",
                    "Check runoff EC and pH",
                    "Ensure proper watering practices",
                ],
            }
            
        primary_diagnosis = matches[0]
        
        return {
            "primary_diagnosis": {
                "deficiency": primary_diagnosis["element"],
                "confidence": f"{primary_diagnosis['confidence']*100:.0f}%",
                "matched_symptoms": primary_diagnosis["matched_symptoms"],
                "solutions": primary_diagnosis["solutions"],
            },
            "differential_diagnoses": matches[1:3] if len(matches) > 1 else [],
            "immediate_actions": [
                "Check and adjust pH to optimal range",
                f"Address {primary_diagnosis['element']} deficiency",
                "Monitor for 3-5 days for improvement",
            ],
            "prevention": [
                "Maintain consistent feeding schedule",
                "Monitor runoff EC and pH",
                "Use quality cal-mag in RO or soft water",
            ],
        }
    
    async def calculate_solution(
        self,
        target_ec: float,
        water_volume_gallons: float,
        growth_phase: str = "late_veg",
        base_water_ec: float = 0.2,
    ) -> Dict[str, Any]:
        """
        Calculate nutrient solution strength.
        
        Provides mixing ratios for target EC.
        """
        try:
            phase = GrowthPhase(growth_phase.lower())
        except ValueError:
            phase = GrowthPhase.LATE_VEG
            
        # Calculate nutrient EC needed (subtract base water EC)
        nutrient_ec = target_ec - base_water_ec
        
        # Generic 3-part nutrient calculation (ml per gallon)
        # Assumes standard 3-part system (Grow/Micro/Bloom)
        npk_ratio = NPK_RATIOS.get(phase, {"N": 2, "P": 2, "K": 2})
        total_parts = npk_ratio["N"] + npk_ratio["P"] + npk_ratio["K"]
        
        if total_parts == 0:
            # Flush phase
            return {
                "phase": phase.value,
                "recommendation": "Flush phase - use plain pH'd water",
                "target_ec": target_ec,
                "water_volume": water_volume_gallons,
            }
            
        # Calculate ml per gallon (scaled by EC)
        base_ml_per_gallon = nutrient_ec * 2.5  # Rough conversion
        
        grow_ml = (npk_ratio["N"] / total_parts) * base_ml_per_gallon * water_volume_gallons
        micro_ml = base_ml_per_gallon * water_volume_gallons * 0.5  # Micro usually constant
        bloom_ml = (npk_ratio["P"] / total_parts) * base_ml_per_gallon * water_volume_gallons
        
        return {
            "target_ec": target_ec,
            "base_water_ec": base_water_ec,
            "nutrient_ec_needed": round(nutrient_ec, 2),
            "water_volume_gallons": water_volume_gallons,
            "water_volume_liters": round(water_volume_gallons * 3.785, 2),
            "growth_phase": phase.value,
            "mixing_order": [
                "1. Fill reservoir with water",
                "2. Add CalMag if using RO/soft water",
                "3. Add Micro/Grow first, stir",
                "4. Add Bloom, stir",
                "5. Adjust pH last",
            ],
            "estimated_amounts": {
                "grow_ml": round(grow_ml, 1),
                "micro_ml": round(micro_ml, 1),
                "bloom_ml": round(bloom_ml, 1),
                "calmag_ml": round(water_volume_gallons * 2, 1),  # ~2ml/gal typical
            },
            "notes": [
                "These are estimates - always verify with EC meter",
                "Start with 50% strength if unsure",
                "Adjust based on plant response",
            ],
        }
    
    async def get_flush_schedule(
        self,
        days_to_harvest: int,
        medium: str = "coco",
    ) -> Dict[str, Any]:
        """
        Get pre-harvest flush schedule.
        
        Provides timeline for flushing nutrients before harvest.
        """
        try:
            med_type = MediumType(medium.lower())
        except ValueError:
            med_type = MediumType.COCO
            
        # Flush duration varies by medium
        flush_durations = {
            MediumType.SOIL: 14,     # 2 weeks
            MediumType.COCO: 7,      # 1 week
            MediumType.HYDRO: 5,     # 5 days
            MediumType.DWC: 5,       # 5 days
            MediumType.RDWC: 5,      # 5 days
        }
        
        flush_days = flush_durations.get(med_type, 7)
        
        if days_to_harvest < flush_days:
            return {
                "warning": f"Less than {flush_days} days to harvest!",
                "recommendation": "Start flush immediately",
                "days_to_harvest": days_to_harvest,
                "optimal_flush_days": flush_days,
            }
            
        start_flush_in = days_to_harvest - flush_days
        
        schedule = []
        for day in range(flush_days):
            if day == 0:
                schedule.append({
                    "day": day + 1,
                    "action": "Heavy flush - 3x pot volume",
                    "ec_target": 0.0,
                    "notes": "Remove all nutrient buildup",
                })
            elif day < flush_days - 2:
                schedule.append({
                    "day": day + 1,
                    "action": "Plain pH'd water",
                    "ec_target": 0.0,
                    "notes": "Water as normal with plain water",
                })
            else:
                schedule.append({
                    "day": day + 1,
                    "action": "Allow slight dry-back",
                    "ec_target": 0.0,
                    "notes": "Stress promotes resin production",
                })
                
        return {
            "medium": med_type.value,
            "days_to_harvest": days_to_harvest,
            "flush_duration_days": flush_days,
            "start_flush_in_days": start_flush_in,
            "start_flush_date": "Calculate from harvest date",
            "schedule": schedule,
            "tips": [
                f"For {med_type.value}, {flush_days} days is optimal",
                "Monitor trichomes - flush when 10-20% amber",
                "Watch for leaf fade - sign of proper flush",
                "Some strains benefit from longer flush",
            ],
        }
    
    def _get_feeding_frequency(self, phase: GrowthPhase, medium: MediumType) -> Dict[str, Any]:
        """Get feeding frequency recommendation"""
        base_frequency = {
            MediumType.SOIL: "Every 2-3 days",
            MediumType.COCO: "Daily or twice daily",
            MediumType.HYDRO: "Continuous",
            MediumType.DWC: "Continuous with weekly res change",
            MediumType.RDWC: "Continuous with weekly res change",
        }
        
        return {
            "frequency": base_frequency.get(medium, "Every 2-3 days"),
            "water_before_dry": medium in [MediumType.COCO, MediumType.HYDRO],
            "allow_dryback": medium == MediumType.SOIL,
        }
    
    def _get_recommended_additives(self, phase: GrowthPhase) -> List[Dict[str, str]]:
        """Get recommended additives for phase"""
        additives = {
            GrowthPhase.SEEDLING: [
                {"name": "Root stimulator", "purpose": "Encourage root development"},
            ],
            GrowthPhase.EARLY_VEG: [
                {"name": "Silica", "purpose": "Strengthen cell walls"},
                {"name": "CalMag", "purpose": "Prevent deficiencies"},
            ],
            GrowthPhase.LATE_VEG: [
                {"name": "Silica", "purpose": "Strengthen stems"},
                {"name": "CalMag", "purpose": "Support growth"},
            ],
            GrowthPhase.TRANSITION: [
                {"name": "PK booster (light)", "purpose": "Prepare for flower"},
            ],
            GrowthPhase.EARLY_FLOWER: [
                {"name": "PK booster", "purpose": "Support flower formation"},
                {"name": "Carbohydrates", "purpose": "Feed beneficial bacteria"},
            ],
            GrowthPhase.MID_FLOWER: [
                {"name": "PK booster (heavy)", "purpose": "Maximize bud development"},
                {"name": "Molasses/carbs", "purpose": "Enhance terpenes"},
            ],
            GrowthPhase.LATE_FLOWER: [
                {"name": "Ripening formula", "purpose": "Promote maturation"},
            ],
            GrowthPhase.FLUSH: [],
        }
        return additives.get(phase, [])
    
    def _get_phase_tips(self, phase: GrowthPhase) -> List[str]:
        """Get tips for current phase"""
        tips = {
            GrowthPhase.SEEDLING: [
                "Keep nutrients light - seedlings are sensitive",
                "High humidity helps at this stage",
                "Don't overwater - let roots search for water",
            ],
            GrowthPhase.EARLY_VEG: [
                "Gradually increase nutrients each week",
                "This is when nitrogen demand is highest",
                "Good time to start training",
            ],
            GrowthPhase.LATE_VEG: [
                "Plants can handle stronger feeds now",
                "Watch for signs of overfeeding",
                "Prepare for transition to flower",
            ],
            GrowthPhase.TRANSITION: [
                "Reduce nitrogen, increase PK",
                "The stretch is coming!",
                "Last chance for training adjustments",
            ],
            GrowthPhase.EARLY_FLOWER: [
                "Focus on phosphorus and potassium",
                "Lower nitrogen to prevent stretching",
                "Bud sites forming - exciting time!",
            ],
            GrowthPhase.MID_FLOWER: [
                "Peak nutrient demand period",
                "Watch for deficiencies closely",
                "Buds fattening up!",
            ],
            GrowthPhase.LATE_FLOWER: [
                "Begin reducing nitrogen completely",
                "Focus on PK and ripening",
                "Start planning flush timing",
            ],
            GrowthPhase.FLUSH: [
                "Plain pH'd water only",
                "Watch for leaf fade - that's good!",
                "Monitor trichomes daily",
            ],
        }
        return tips.get(phase, ["Maintain consistent feeding schedule"])


# Register agent
AgentRegistry.register(NutrientAdvisorAgent())
