from .plant_health_vision import PlantHealthVisionAgent
from ..base import AgentRegistry, AgentContext, AgentResult
from typing import Dict, Any, Optional

class PlantHealthActionVariant(PlantHealthVisionAgent):
    """
    Base class for A/B testing variants of PlantHealthVisionAgent.
    Allows overriding the analysis prompt strategy.
    """
    def __init__(self, variant_id: str, strategy_name: str, description: str):
        super().__init__()
        self.agent_id = f"plant_health_{variant_id}"
        self.name = f"Plant Health ({strategy_name})"
        self.description = description
        self.strategy_name = strategy_name

    def _build_analysis_prompt(self, growth_stage: str) -> str:
        raise NotImplementedError

class PlantHealthCOT(PlantHealthActionVariant):
    """
    Variant A: Chain-of-Thought (CoT) Strategy.
    Encourages detailed reasoning before making function calls.
    """
    def __init__(self):
        super().__init__(
            variant_id="cot", 
            strategy_name="Reasoning",
            description="Uses detailed Chain-of-Thought reasoning before actions"
        )

    def _build_analysis_prompt(self, growth_stage: str) -> str:
        return f"""Analyze this plant (Stage: {growth_stage}).
        
        step-by-step:
        1. Identify visible symptoms.
        2. Correlate with common issues (N-P-K, pests).
        3. Rate severity (Low/Med/High).
        4. Formulate a treatment plan.
        
        Output detailed reasoning in <think> tags, then call functions.
        """

class PlantHealthDirect(PlantHealthActionVariant):
    """
    Variant B: Direct Action Strategy.
    Focuses on immediate, concise function calling for speed.
    """
    def __init__(self):
        super().__init__(
            variant_id="direct", 
            strategy_name="Fast Action",
            description="Optimized for speed and direct function execution"
        )

    def _build_analysis_prompt(self, growth_stage: str) -> str:
        return f"""Plant Stage: {growth_stage}.
        
        Detect issues immediately.
        If found, call get_treatment_plan.
        If healthy, call award_xp.
        
        Be concise. Use <think> only for critical disambiguation.
        """

# Register Variants
def register_variants():
    AgentRegistry.register(PlantHealthCOT())
    AgentRegistry.register(PlantHealthDirect())
