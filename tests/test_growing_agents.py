"""Test script for Growing Agents"""
import asyncio
from app.agents.growing import VPDOptimizerAgent, NutrientAdvisorAgent

async def test_vpd():
    print("=== VPD Optimizer Test ===")
    vpd = VPDOptimizerAgent()
    result = await vpd.calculate_vpd(temperature=78, humidity=55, growth_stage='mid_flower')
    print(f"VPD: {result['vpd']} kPa")
    print(f"Status: {result['status']}")
    print(f"Zone: {result['zone']['name']}")
    print(f"Optimal Range: {result['optimal_range']}")
    
    rec = await vpd.get_vpd_recommendation(
        current_vpd=result['vpd'], 
        temperature=78, 
        humidity=55, 
        growth_stage='mid_flower'
    )
    print(f"Summary: {rec['summary']}")
    return True

async def test_nutrient():
    print("\n=== Nutrient Advisor Test ===")
    nutrient = NutrientAdvisorAgent()
    schedule = await nutrient.get_feeding_schedule(
        growth_phase='mid_flower', 
        medium='coco', 
        week_in_phase=3
    )
    print(f"Phase: {schedule['growth_phase']}")
    print(f"EC Target: {schedule['ec_target']}")
    print(f"pH Range: {schedule['ph_range']}")
    print(f"NPK Ratio: {schedule['npk_ratio']}")
    
    diagnosis = await nutrient.diagnose_deficiency(
        symptoms=['yellowing lower leaves', 'pale green'], 
        affected_area='lower leaves'
    )
    print(f"\nPrimary Diagnosis: {diagnosis['primary_diagnosis']['deficiency']}")
    print(f"Confidence: {diagnosis['primary_diagnosis']['confidence']}")
    return True

async def main():
    await test_vpd()
    await test_nutrient()
    print("\n✅ All tests passed!")

if __name__ == "__main__":
    asyncio.run(main())
