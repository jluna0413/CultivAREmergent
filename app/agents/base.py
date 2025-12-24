"""
CultivAR Agent Base Framework

Integrates:
- EvoAgentX: Feedback learning, outcome tracking, A/B evolution
- BMAD-Method: Workflow orchestration, role-based agents
- Swarm: Parallel task execution
- Hive-Mind: Collective intelligence aggregation
- Sequential Thinking: Complex decision chains
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type
import asyncio
import json
import logging

logger = logging.getLogger(__name__)


class AgentRole(Enum):
    """Agent roles aligned with BMAD-Method personas"""
    DISCOVERY = "discovery"      # Marketplace, Strain Sommelier, Rarity Hunter
    PLANNING = "planning"        # Grow Planner, Environment Matcher
    GROWING = "growing"          # Plant Health, VPD, Nutrient Advisor
    HARVEST = "harvest"          # Harvest Timing, Cure Coach, Yield Logger
    COMMUNITY = "community"      # NFT Marketplace, Grow Buddy, Reputation
    MARKETING = "marketing"      # Content Creator, Social Media, Email
    ORCHESTRATOR = "orchestrator"  # BMad Orchestrator pattern


class ExecutionMode(Enum):
    """Execution patterns for agent tasks"""
    SEQUENTIAL = "sequential"    # One-by-one execution
    SWARM = "swarm"             # Parallel execution with aggregation
    HIVE_MIND = "hive_mind"     # Collective decision making
    EVOLUTION = "evolution"      # A/B testing with winner selection


@dataclass
class AgentContext:
    """Shared context passed between agents in multi-agent workflows"""
    user_id: int
    session_id: str
    plant_ids: List[int] = field(default_factory=list)
    sensor_data: Dict[str, Any] = field(default_factory=dict)
    conversation_history: List[Dict] = field(default_factory=list)
    xp_earned: int = 0
    achievements_unlocked: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResult:
    """Standardized result from agent execution"""
    success: bool
    agent_id: str
    output: Any
    confidence: float = 1.0
    xp_reward: int = 0
    next_actions: List[str] = field(default_factory=list)
    feedback_required: bool = False
    execution_time_ms: int = 0
    error: Optional[str] = None


@dataclass
class EvolutionMetrics:
    """EvoAgentX metrics for agent performance tracking"""
    agent_id: str
    total_executions: int = 0
    successful_executions: int = 0
    user_feedback_positive: int = 0
    user_feedback_negative: int = 0
    avg_confidence: float = 0.0
    outcome_accuracy: float = 0.0  # How often predictions matched reality
    
    @property
    def success_rate(self) -> float:
        if self.total_executions == 0:
            return 0.0
        return self.successful_executions / self.total_executions
    
    @property
    def feedback_score(self) -> float:
        total = self.user_feedback_positive + self.user_feedback_negative
        if total == 0:
            return 0.5  # Neutral
        return self.user_feedback_positive / total


class BaseAgent(ABC):
    """
    Base class for all CultivAR agents.
    
    Implements:
    - BMAD-Method: Role-based identity with commands and dependencies
    - EvoAgentX: Performance tracking and feedback learning
    - MCP Tools: Tool registration for external access
    """
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        role: AgentRole,
        description: str,
    ):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.description = description
        self.metrics = EvolutionMetrics(agent_id=agent_id)
        self._tools: Dict[str, Callable] = {}
        self._dependencies: List[str] = []
        
    @abstractmethod
    async def execute(self, context: AgentContext, **kwargs) -> AgentResult:
        """Execute the agent's primary function"""
        pass
    
    def register_tool(self, name: str, func: Callable, description: str = ""):
        """Register a tool for MCP exposure"""
        self._tools[name] = {
            "function": func,
            "description": description,
        }
        
    def get_tools(self) -> Dict[str, Any]:
        """Get all registered tools for MCP server"""
        return self._tools
    
    def record_execution(self, result: AgentResult):
        """EvoAgentX: Record execution for learning"""
        self.metrics.total_executions += 1
        if result.success:
            self.metrics.successful_executions += 1
        # Update rolling average confidence
        n = self.metrics.total_executions
        self.metrics.avg_confidence = (
            (self.metrics.avg_confidence * (n - 1) + result.confidence) / n
        )
        
    def record_feedback(self, positive: bool):
        """EvoAgentX: Record user feedback"""
        if positive:
            self.metrics.user_feedback_positive += 1
        else:
            self.metrics.user_feedback_negative += 1
            
    def record_outcome(self, prediction: Any, actual: Any, match: bool):
        """EvoAgentX: Track prediction accuracy"""
        n = self.metrics.total_executions
        if n > 0:
            current_accuracy = self.metrics.outcome_accuracy
            self.metrics.outcome_accuracy = (
                (current_accuracy * (n - 1) + (1.0 if match else 0.0)) / n
            )


class SwarmExecutor:
    """
    Swarm pattern: Execute multiple agents in parallel and aggregate results.
    
    Use cases:
    - Running multiple analysis agents on same data
    - Gathering recommendations from multiple specialists
    - Parallel data fetching
    """
    
    def __init__(self, agents: List[BaseAgent]):
        self.agents = agents
        
    async def execute_all(
        self, 
        context: AgentContext,
        aggregation_strategy: str = "vote",
        **kwargs
    ) -> List[AgentResult]:
        """Execute all agents in parallel"""
        tasks = [
            agent.execute(context, **kwargs) 
            for agent in self.agents
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions
        valid_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Agent {self.agents[i].agent_id} failed: {result}")
                valid_results.append(AgentResult(
                    success=False,
                    agent_id=self.agents[i].agent_id,
                    output=None,
                    error=str(result)
                ))
            else:
                valid_results.append(result)
                
        return valid_results
    
    async def execute_with_consensus(
        self,
        context: AgentContext,
        min_agreement: float = 0.6,
        **kwargs
    ) -> AgentResult:
        """
        Hive-Mind pattern: Execute all and find consensus.
        
        Returns the result with highest agreement among agents.
        """
        results = await self.execute_all(context, **kwargs)
        successful = [r for r in results if r.success]
        
        if not successful:
            return AgentResult(
                success=False,
                agent_id="swarm",
                output=None,
                error="No agents succeeded"
            )
        
        # Simple voting: Count matching outputs
        output_votes: Dict[str, List[AgentResult]] = {}
        for result in successful:
            key = json.dumps(result.output, sort_keys=True, default=str)
            if key not in output_votes:
                output_votes[key] = []
            output_votes[key].append(result)
        
        # Find winner
        winner_key = max(output_votes.keys(), key=lambda k: len(output_votes[k]))
        winner_votes = output_votes[winner_key]
        agreement = len(winner_votes) / len(successful)
        
        if agreement < min_agreement:
            return AgentResult(
                success=False,
                agent_id="swarm",
                output=None,
                confidence=agreement,
                error=f"Insufficient consensus ({agreement:.0%} < {min_agreement:.0%})"
            )
        
        # Return winning result with aggregated confidence
        avg_confidence = sum(r.confidence for r in winner_votes) / len(winner_votes)
        return AgentResult(
            success=True,
            agent_id="swarm_consensus",
            output=winner_votes[0].output,
            confidence=avg_confidence * agreement,
            xp_reward=sum(r.xp_reward for r in successful),
        )


class EvolutionExecutor:
    """
    EvoAgentX pattern: A/B test agent strategies and evolve.
    
    Use cases:
    - Testing different recommendation algorithms
    - Evolving prompt strategies
    - Optimizing agent parameters
    """
    
    def __init__(self, agent_variants: List[BaseAgent]):
        self.variants = agent_variants
        self.performance_history: Dict[str, List[float]] = {
            agent.agent_id: [] for agent in agent_variants
        }
        
    async def execute_best(
        self,
        context: AgentContext,
        exploration_rate: float = 0.1,
        **kwargs
    ) -> AgentResult:
        """
        Execute the best-performing variant with occasional exploration.
        
        Uses epsilon-greedy strategy for exploration/exploitation balance.
        """
        import random
        
        # Exploration: Random agent
        if random.random() < exploration_rate:
            agent = random.choice(self.variants)
        else:
            # Exploitation: Best performer
            agent = max(
                self.variants,
                key=lambda a: a.metrics.feedback_score * a.metrics.success_rate
            )
        
        result = await agent.execute(context, **kwargs)
        agent.record_execution(result)
        
        return result
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comparative performance of all variants"""
        return {
            agent.agent_id: {
                "success_rate": agent.metrics.success_rate,
                "feedback_score": agent.metrics.feedback_score,
                "avg_confidence": agent.metrics.avg_confidence,
                "outcome_accuracy": agent.metrics.outcome_accuracy,
                "total_executions": agent.metrics.total_executions,
            }
            for agent in self.variants
        }


class SequentialThinkingExecutor:
    """
    Sequential Thinking pattern: Chain of thought execution.
    
    Use cases:
    - Complex multi-step analysis
    - Decision trees with branching
    - Progressive refinement
    """
    
    def __init__(self):
        self.thought_chain: List[Dict] = []
        
    async def think_step(
        self,
        thought_number: int,
        total_thoughts: int,
        thought: str,
        agent: BaseAgent,
        context: AgentContext,
        is_revision: bool = False,
        revises_thought: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute a single thought step"""
        
        step = {
            "thought_number": thought_number,
            "total_thoughts": total_thoughts,
            "thought": thought,
            "agent_id": agent.agent_id,
            "is_revision": is_revision,
            "revises_thought": revises_thought,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        # Execute agent for this thought
        result = await agent.execute(context, thought=thought, **kwargs)
        step["result"] = {
            "success": result.success,
            "output": result.output,
            "confidence": result.confidence,
        }
        
        self.thought_chain.append(step)
        
        return {
            "step": step,
            "next_thought_needed": thought_number < total_thoughts,
            "needs_revision": result.confidence < 0.7,
            "thought_history_length": len(self.thought_chain),
        }
    
    def get_final_conclusion(self) -> Optional[Any]:
        """Get the conclusion from the thought chain"""
        if not self.thought_chain:
            return None
        return self.thought_chain[-1].get("result", {}).get("output")


# Agent Registry - BMAD-Method style discovery
class AgentRegistry:
    """
    Central registry for all CultivAR agents.
    
    Provides:
    - Agent discovery by role/capability
    - MCP tool aggregation
    - Workflow orchestration
    """
    
    _instance = None
    _agents: Dict[str, BaseAgent] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def register(cls, agent: BaseAgent):
        """Register an agent"""
        cls._agents[agent.agent_id] = agent
        logger.info(f"Registered agent: {agent.agent_id} ({agent.role.value})")
        
    @classmethod
    def get(cls, agent_id: str) -> Optional[BaseAgent]:
        """Get agent by ID"""
        return cls._agents.get(agent_id)
    
    @classmethod
    def get_by_role(cls, role: AgentRole) -> List[BaseAgent]:
        """Get all agents with a specific role"""
        return [a for a in cls._agents.values() if a.role == role]
    
    @classmethod
    def get_all(cls) -> List[BaseAgent]:
        """Get all registered agents"""
        return list(cls._agents.values())
    
    @classmethod
    def get_all_tools(cls) -> Dict[str, Any]:
        """Aggregate all tools from all agents for MCP server"""
        all_tools = {}
        for agent in cls._agents.values():
            for name, tool in agent.get_tools().items():
                all_tools[f"{agent.agent_id}.{name}"] = tool
        return all_tools
    
    @classmethod
    def create_swarm(cls, role: AgentRole) -> SwarmExecutor:
        """Create a swarm executor for a role"""
        agents = cls.get_by_role(role)
        return SwarmExecutor(agents)
