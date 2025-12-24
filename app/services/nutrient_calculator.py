"""
Nutrient Calculator Service
Core logic for nutrient mixing calculations and recommendations.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class GrowthStage(str, Enum):
    """Plant growth stages."""
    SEEDLING = "seedling"
    EARLY_VEG = "early_veg"
    LATE_VEG = "late_veg"
    TRANSITION = "transition"
    EARLY_FLOWER = "early_flower"
    MID_FLOWER = "mid_flower"
    LATE_FLOWER = "late_flower"
    FLUSH = "flush"


class GrowMedium(str, Enum):
    """Growing mediums."""
    HYDRO = "hydro"
    COCO = "coco"
    SOIL = "soil"
    INERT = "inert"  # perlite, rockwool, etc.


class WaterType(str, Enum):
    """Water source types."""
    TAP = "tap"
    DISTILLED = "distilled"
    RO = "ro"  # Reverse osmosis
    RE_MINERALIZED = "re_mineralized"  # RO + minerals added back


class FeedingStrength(str, Enum):
    """Feeding strength levels."""
    LIGHT = "light"  # 50%
    MEDIUM = "medium"  # 75%
    AGGRESSIVE = "aggressive"  # 100%
    CUSTOM = "custom"


@dataclass
class NutrientMix:
    """Calculated nutrient mix result."""
    components: Dict[str, float]  # {component_name: ml_amount}
    total_volume_liters: float
    ppm_target: Tuple[float, float]  # (min, max)
    ec_target: Tuple[float, float]  # (min, max)
    ph_target: Tuple[float, float]  # (min, max)
    mixing_instructions: List[str]
    requires_calmag: bool
    calmag_ml: Optional[float] = None


class NutrientCalculator:
    """
    Nutrient calculator service.
    Handles calculation logic for nutrient mixing.
    """

    # Feeding strength multipliers
    STRENGTH_MULTIPLIERS = {
        FeedingStrength.LIGHT: 0.5,
        FeedingStrength.MEDIUM: 0.75,
        FeedingStrength.AGGRESSIVE: 1.0,
    }

    # CalMag recommendations by water type (ml per liter)
    CALMAG_RECOMMENDATIONS = {
        WaterType.RO: 0.5,
        WaterType.DISTILLED: 0.5,
        WaterType.RE_MINERALIZED: 0.25,
        WaterType.TAP: 0.0,
    }

    # PPM conversion factor (500 scale)
    EC_TO_PPM_500 = 500

    @staticmethod
    def calculate_mix(
        formula_ratios: Dict[int, float],  # {component_id: ml_per_liter}
        component_names: Dict[int, str],  # {component_id: name}
        tank_size_liters: float,
        feeding_strength: FeedingStrength,
        water_type: WaterType,
        ppm_range: Tuple[float, float],
        ec_range: Tuple[float, float],
        ph_range: Tuple[float, float],
        custom_strength: Optional[float] = None,
    ) -> NutrientMix:
        """
        Calculate nutrient mix for given parameters.

        Args:
            formula_ratios: Base ratios per liter
            component_names: Component ID to name mapping
            tank_size_liters: Reservoir/container size
            feeding_strength: Strength preset
            water_type: Water source type
            ppm_range: Target PPM range (min, max)
            ec_range: Target EC range (min, max)
            ph_range: Target pH range (min, max)
            custom_strength: Strength multiplier if using CUSTOM

        Returns:
            NutrientMix with calculated amounts and instructions
        """
        # Determine strength multiplier
        if feeding_strength == FeedingStrength.CUSTOM and custom_strength:
            multiplier = custom_strength
        else:
            multiplier = NutrientCalculator.STRENGTH_MULTIPLIERS.get(feeding_strength, 1.0)

        # Calculate component amounts
        components = {}
        for component_id, ml_per_liter in formula_ratios.items():
            component_name = component_names.get(component_id, f"Component {component_id}")
            total_ml = ml_per_liter * tank_size_liters * multiplier
            components[component_name] = round(total_ml, 2)

        # CalMag calculation
        requires_calmag = water_type in [WaterType.RO, WaterType.DISTILLED, WaterType.RE_MINERALIZED]
        calmag_ml = None
        if requires_calmag:
            calmag_per_liter = NutrientCalculator.CALMAG_RECOMMENDATIONS[water_type]
            calmag_ml = round(calmag_per_liter * tank_size_liters, 2)

        # Adjust PPM/EC targets based on strength
        ppm_min = ppm_range[0] * multiplier
        ppm_max = ppm_range[1] * multiplier
        ec_min = ec_range[0] * multiplier
        ec_max = ec_range[1] * multiplier

        # Generate mixing instructions
        instructions = NutrientCalculator._generate_instructions(
            components=components,
            tank_size=tank_size_liters,
            requires_calmag=requires_calmag,
            calmag_ml=calmag_ml,
            ph_range=ph_range,
        )

        return NutrientMix(
            components=components,
            total_volume_liters=tank_size_liters,
            ppm_target=(round(ppm_min, 1), round(ppm_max, 1)),
            ec_target=(round(ec_min, 2), round(ec_max, 2)),
            ph_target=ph_range,
            mixing_instructions=instructions,
            requires_calmag=requires_calmag,
            calmag_ml=calmag_ml,
        )

    @staticmethod
    def _generate_instructions(
        components: Dict[str, float],
        tank_size: float,
        requires_calmag: bool,
        calmag_ml: Optional[float],
        ph_range: Tuple[float, float],
    ) -> List[str]:
        """Generate step-by-step mixing instructions."""
        instructions = [
            f"1. Fill reservoir with {tank_size}L of water",
        ]

        step = 2
        if requires_calmag and calmag_ml:
            instructions.append(f"{step}. Add {calmag_ml}ml CalMag supplement")
            step += 1

        # Sort components for consistent order
        sorted_components = sorted(components.items())

        for component_name, ml_amount in sorted_components:
            instructions.append(f"{step}. Add {ml_amount}ml of {component_name}")
            step += 1

        instructions.extend([
            f"{step}. Mix thoroughly and let sit for 15 minutes",
            f"{step + 1}. Check and adjust pH to {ph_range[0]}-{ph_range[1]}",
            f"{step + 2}. Verify EC/PPM is within target range",
            f"{step + 3}. Feed plants or store in dark, cool location",
        ])

        return instructions

    @staticmethod
    def ec_to_ppm(ec: float, scale: int = 500) -> float:
        """Convert EC to PPM."""
        return ec * scale

    @staticmethod
    def ppm_to_ec(ppm: float, scale: int = 500) -> float:
        """Convert PPM to EC."""
        return ppm / scale

    @staticmethod
    def get_ph_recommendations(medium: GrowMedium) -> Tuple[float, float]:
        """Get pH range recommendations by medium."""
        recommendations = {
            GrowMedium.HYDRO: (5.5, 6.5),
            GrowMedium.COCO: (5.8, 6.5),
            GrowMedium.SOIL: (6.0, 7.0),
            GrowMedium.INERT: (5.5, 6.5),
        }
        return recommendations.get(medium, (5.8, 6.5))

    @staticmethod
    def calculate_ingredient_cost(
        components: Dict[str, float],  # {component_name: ml_used}
        inventory: Dict[str, Dict],  # {component_name: {quantity_ml, cost, original_quantity}}
    ) -> Optional[float]:
        """
        Calculate cost of nutrients used in this feeding.
        
        Args:
            components: Components used with amounts
            inventory: User's inventory data with costs
            
        Returns:
            Estimated cost of the feeding, or None if insufficient data
        """
        total_cost = 0.0
        
        for component_name, ml_used in components.items():
            inv = inventory.get(component_name)
            if not inv or not inv.get('cost') or not inv.get('original_quantity_ml'):
                return None  # Can't calculate without complete data
                
            cost_per_ml = inv['cost'] / inv['original_quantity_ml']
            total_cost += cost_per_ml * ml_used
        
        return round(total_cost, 2)

    @staticmethod
    def check_inventory_sufficient(
        components: Dict[str, float],  # {component_name: ml_needed}
        inventory: Dict[str, float],  # {component_name: ml_available}
    ) -> Tuple[bool, List[str]]:
        """
        Check if user has enough nutrients in inventory.
        
        Args:
            components: Required amounts
            inventory: Available amounts
            
        Returns:
            (is_sufficient, list_of_insufficient_items)
        """
        insufficient = []
        
        for component_name, ml_needed in components.items():
            ml_available = inventory.get(component_name, 0.0)
            if ml_available < ml_needed:
                insufficient.append(
                    f"{component_name}: need {ml_needed}ml, have {ml_available}ml"
                )
        
        return len(insufficient) == 0, insufficient
