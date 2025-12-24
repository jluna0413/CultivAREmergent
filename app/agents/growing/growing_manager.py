"""
Growing Operations Manager Agent

The "Brain" of the growing operation.
Uses FunctionGemma to reason about user needs and coordinate:
- Vision Analysis (PlantHealthVisionAgent)
- Environmental Control (VPDOptimizerAgent)
- Gamification (XP/Rewards)

This agent parses natural language, decides on actions, and executes them via tool calls.
"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from ..base import (
    BaseAgent,
    AgentRole,
    AgentContext,
    AgentResult,
    AgentRegistry,
)
from ...ml.model_loader import get_model_loader
from ...ml.function_gemma_utils import FunctionGemmaParser

logger = logging.getLogger(__name__)

class GrowingOperationsAgent(BaseAgent):
    """
    Orchestrator for all growing-related tasks.
    Leverages FunctionGemma for high-level reasoning and tool selection.
    """
    
    def __init__(self):
        super().__init__(
            agent_id="growing_manager",
            name="Growing Operations Manager",
            role=AgentRole.GROWING,  # Acts as a manager within the growing domain
            description="Intelligent orchestrator for plant care and environment management",
        )
        
        # This agent DOES NOT register its own domain tools.
        # Instead, it knows how to CALL other agents' tools.
        # It's the "User Interface" agent for complex requests.

    async def execute(self, context: AgentContext, **kwargs) -> AgentResult:
        """
        Execute high-level reasoning loop.
        1. Receive use query/context.
        2. Use FunctionGemma to decide on tools.
        3. Execute tools (which call other agents).
        4. Synthesize result.
        """
        user_query = kwargs.get("query") or kwargs.get("message")
        
        if not user_query:
            return AgentResult(success=False, error="No query provided")

        try:
            # 1. Get FunctionGemma Reasoning
            actions = await self._reason_about_request(user_query, context)
            
            # 2. Execute Planned Actions
            results = []
            for call in actions.get("function_calls", []):
                tool_name = call["name"]
                tool_args = call["arguments"]
                
                # Execute tool using the Registry's tool router
                # (In a real system, we'd have a formal router, here we simulate)
                result = await self._execute_tool_safely(tool_name, tool_args, context)
                results.append(result)
            
            return AgentResult(
                success=True,
                output={
                    "reasoning": actions.get("reasoning"),
                    "actions_taken": results
                },
                agent_id=self.agent_id
            )
            
        except Exception as e:
            logger.error(f"Operations Manager Error: {e}")
            return AgentResult(success=False, error=str(e))

    async def _reason_about_request(self, query: str, context: AgentContext) -> Dict[str, Any]:
        """
        Use FunctionGemma local model to plan actions.
        """
        model_loader = get_model_loader()
        
        # Build prompt with available tools context
        # In a real Unsloth deployment, the model knows its tools via fine-tuning
        # but we provide the system prompt / schema here or in the model loader.
        
        prompt = f"""<start_of_turn>user
{query}
Context: Plant IDs {context.plant_ids}. 
Available Tools: analyze_plant_health, optimize_environment, award_xp, get_treatment_plan.
<end_of_turn>
<start_of_turn>model
"""
        
        # Call Local FunctionGemma (or mock if not ready)
        # Note: We use a specialized method if available, or standard generation
        response_text = await model_loader.generate(prompt, max_tokens=512)
        
        # Parse output
        return FunctionGemmaParser.parse_response(response_text)

    async def _execute_tool_safely(self, tool_name: str, args: Dict, context: AgentContext) -> Any:
        """Find and execute the requested tool."""
        # Find the agent that owns this tool
        # In reality, AgentRegistry would expose a get_tool method
        tool = AgentRegistry.get_tool(tool_name)
        
        if not tool:
            return {"error": f"Tool {tool_name} not found"}
            
        return await tool(context, **args)

# Register Manager
AgentRegistry.register(GrowingOperationsAgent())
