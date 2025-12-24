"""
Agronomic calculations utility module.
"""
import math


def calculate_vpd(air_temp_f: float, relative_humidity: float, leaf_temp_offset_f: float = -2.0) -> float:
    """
    Calculate Vapor Pressure Deficit (VPD) in kPa.

    Args:
        air_temp_f: Air temperature in Fahrenheit.
        relative_humidity: Relative humidity in percent (0-100).
        leaf_temp_offset_f: Difference between leaf temp and air temp in Fahrenheit (default: -2.0).

    Returns:
        float: VPD in kPa, rounded to 2 decimal places.
    """
    # 1. Convert Temps to Celsius
    air_temp_c = (air_temp_f - 32) * 5.0 / 9.0
    leaf_temp_c = ((air_temp_f + leaf_temp_offset_f) - 32) * 5.0 / 9.0

    # 2. Calculate Saturation Vapor Pressure (SVP) at AIR temperature
    # Formula: 0.61078 * exp(17.27 * T / (T + 237.3))
    svp_air = 0.61078 * math.exp((17.27 * air_temp_c) / (air_temp_c + 237.3))

    # 3. Calculate Saturation Vapor Pressure (SVP) at LEAF temperature
    svp_leaf = 0.61078 * math.exp((17.27 * leaf_temp_c) / (leaf_temp_c + 237.3))

    # 4. Calculate Actual Vapor Pressure (AVP) of the air
    # VP = SVP_air * (RH / 100)
    avp = svp_air * (relative_humidity / 100.0)

    # 5. Calculate VPD
    # VPD = SVP_leaf - AVP_air
    vpd = svp_leaf - avp

    # Ensure non-negative
    return max(0.0, round(vpd, 2))
