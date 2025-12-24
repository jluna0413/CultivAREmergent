"""
Agent Dashboard API Routes

FastAPI endpoints for the Agent Testing Dashboard.
Supports parallel swarm execution for rapid validation.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
import asyncio
import time

# Import agent infrastructure
from app.agents.base import AgentRegistry, AgentContext, AgentResult

# Import all agents to register them
from app.agents.discovery import (
    StrainSommelierAgent, MarketplaceChatbotAgent, 
    BreederSpotlightAgent, RarityHunterAgent
)
from app.agents.growing import (
    PlantHealthVisionAgent, DailyCheckInAgent,
    VPDOptimizerAgent, NutrientAdvisorAgent,
    YieldEstimatorAgent
)
from app.agents.community import (
    NFTMarketplaceAgent, GrowBuddyAgent, ReputationTrackerAgent
)

router = APIRouter(prefix="/api/v2/agents", tags=["agents"])


class AgentRequest(BaseModel):
    """Request to execute an agent"""
    agent_id: str
    action: str = "default"
    params: Dict[str, Any] = Field(default_factory=dict)
    user_id: Optional[int] = 1


class SwarmRequest(BaseModel):
    """Request to execute multiple agents in parallel"""
    agents: List[AgentRequest]
    timeout_seconds: int = 30


class AgentResponse(BaseModel):
    """Response from agent execution"""
    success: bool
    agent_id: str
    agent_name: str
    output: Any
    error: Optional[str] = None
    execution_time_ms: float
    xp_reward: int = 0


class SwarmResponse(BaseModel):
    """Response from swarm execution"""
    total_agents: int
    successful: int
    failed: int
    total_time_ms: float
    results: List[AgentResponse]


@router.get("/list")
async def list_agents():
    """List all registered agents"""
    agents = AgentRegistry.get_all()
    return {
        "total": len(agents),
        "agents": [
            {
                "id": a.agent_id,
                "name": a.name,
                "role": a.role.value,
                "description": a.description,
                "tools": list(a.tools.keys()) if hasattr(a, 'tools') else [],
            }
            for a in agents
        ]
    }


@router.post("/execute", response_model=AgentResponse)
async def execute_agent(request: AgentRequest):
    """Execute a single agent"""
    start = time.time()
    
    agent = AgentRegistry.get(request.agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{request.agent_id}' not found")
    
    context = AgentContext(
        user_id=request.user_id,
        session_id="dashboard-test",
        metadata={"source": "dashboard"},
    )
    
    try:
        result = await agent.execute(context, action=request.action, **request.params)
        return AgentResponse(
            success=result.success,
            agent_id=agent.agent_id,
            agent_name=agent.name,
            output=result.output,
            error=result.error,
            execution_time_ms=(time.time() - start) * 1000,
            xp_reward=result.xp_reward or 0,
        )
    except Exception as e:
        return AgentResponse(
            success=False,
            agent_id=agent.agent_id,
            agent_name=agent.name,
            output=None,
            error=str(e),
            execution_time_ms=(time.time() - start) * 1000,
        )


@router.post("/swarm", response_model=SwarmResponse)
async def execute_swarm(request: SwarmRequest):
    """Execute multiple agents in parallel (swarm pattern)"""
    start = time.time()
    
    async def run_agent(req: AgentRequest) -> AgentResponse:
        agent_start = time.time()
        agent = AgentRegistry.get(req.agent_id)
        
        if not agent:
            return AgentResponse(
                success=False,
                agent_id=req.agent_id,
                agent_name="Unknown",
                output=None,
                error=f"Agent '{req.agent_id}' not found",
                execution_time_ms=0,
            )
        
        context = AgentContext(
            user_id=req.user_id,
            session_id="swarm-test",
            metadata={"source": "swarm"},
        )
        
        try:
            result = await asyncio.wait_for(
                agent.execute(context, action=req.action, **req.params),
                timeout=request.timeout_seconds
            )
            return AgentResponse(
                success=result.success,
                agent_id=agent.agent_id,
                agent_name=agent.name,
                output=result.output,
                error=result.error,
                execution_time_ms=(time.time() - agent_start) * 1000,
                xp_reward=result.xp_reward or 0,
            )
        except asyncio.TimeoutError:
            return AgentResponse(
                success=False,
                agent_id=agent.agent_id,
                agent_name=agent.name,
                output=None,
                error="Timeout",
                execution_time_ms=(time.time() - agent_start) * 1000,
            )
        except Exception as e:
            return AgentResponse(
                success=False,
                agent_id=agent.agent_id,
                agent_name=agent.name,
                output=None,
                error=str(e),
                execution_time_ms=(time.time() - agent_start) * 1000,
            )
    
    # Execute all agents in parallel
    results = await asyncio.gather(*[run_agent(req) for req in request.agents])
    
    successful = sum(1 for r in results if r.success)
    
    return SwarmResponse(
        total_agents=len(results),
        successful=successful,
        failed=len(results) - successful,
        total_time_ms=(time.time() - start) * 1000,
        results=results,
    )


@router.post("/test-all")
async def test_all_agents():
    """Run a quick test on all registered agents"""
    agents = AgentRegistry.get_all()
    
    # Build test requests for each agent
    test_requests = []
    for agent in agents:
        params = {}
        action = "default"
        
        # Agent-specific test parameters
        if agent.agent_id == "vpd_optimizer":
            action = "calculate"
            params = {"temperature": 78, "humidity": 55}
        elif agent.agent_id == "nutrient_advisor":
            action = "schedule"
            params = {"growth_phase": "veg", "medium": "coco"}
        elif agent.agent_id == "yield_estimator":
            action = "estimate"
            params = {"light_watts": 400, "space_sqft": 16}
        elif agent.agent_id == "marketplace_chatbot":
            action = "search"
            params = {"query": "relaxing indica"}
        elif agent.agent_id == "nft_marketplace":
            action = "verify"
            params = {"wallet_address": "FOUNDER123"}
        elif agent.agent_id == "grow_buddy":
            action = "advice"
            params = {"topic": "watering", "experience_level": "beginner"}
        elif agent.agent_id == "reputation_tracker":
            action = "get"
            params = {"user_id": 1}
        elif agent.agent_id == "breeder_spotlight":
            action = "spotlight"
            params = {}
        elif agent.agent_id == "rarity_hunter":
            action = "find"
            params = {"min_rarity": "rare"}
        elif agent.agent_id == "strain_sommelier":
            action = "recommend"
            params = {"preferences": {"effect": "relaxing"}}
        elif agent.agent_id == "daily_checkin":
            action = "checkin"
            params = {"plant_id": 1}
        elif agent.agent_id == "plant_health_vision":
            action = "analyze_plant_photo"  # Corrected action name from 'analyze'
            params = {
                "image_data": "base64_mock_data", 
                "image_description": "healthy green leaves"
            }
            
        test_requests.append(AgentRequest(
            agent_id=agent.agent_id,
            action=action,
            params=params,
        ))
    
    # Execute swarm
    swarm_request = SwarmRequest(agents=test_requests)
    return await execute_swarm(swarm_request)


# Quick test endpoints for individual agent categories
@router.get("/test/discovery")
async def test_discovery_agents():
    """Quick test of discovery agents"""
    test_requests = [
        AgentRequest(agent_id="strain_sommelier", action="recommend", params={"preferences": {"effect": "energetic"}}),
        AgentRequest(agent_id="marketplace_chatbot", action="search", params={"query": "high THC sativa"}),
        AgentRequest(agent_id="breeder_spotlight", action="spotlight", params={}),
        AgentRequest(agent_id="rarity_hunter", action="find", params={"min_rarity": "legendary"}),
    ]
    return await execute_swarm(SwarmRequest(agents=test_requests))


@router.get("/test/growing")
async def test_growing_agents():
    """Quick test of growing agents"""
    test_requests = [
        AgentRequest(agent_id="vpd_optimizer", action="calculate", params={"temperature": 80, "humidity": 60}),
        AgentRequest(agent_id="nutrient_advisor", action="schedule", params={"growth_phase": "flower", "medium": "soil"}),
        AgentRequest(agent_id="daily_checkin", action="checkin", params={"plant_id": 1}),
        AgentRequest(agent_id="yield_estimator", action="estimate", params={"light_watts": 600, "space_sqft": 25}),
        AgentRequest(
            agent_id="plant_health_vision", 
            action="analyze_plant_photo", 
            params={
                "image_data": "base64_mock_data",
                "image_description": "yellowing lower leaves"
            }
        ),
    ]
    return await execute_swarm(SwarmRequest(agents=test_requests))


@router.get("/test/community")
async def test_community_agents():
    """Quick test of community agents"""
    test_requests = [
        AgentRequest(agent_id="nft_marketplace", action="verify", params={"wallet_address": "FOUNDER999"}),
        AgentRequest(agent_id="grow_buddy", action="tip", params={"experience_level": "intermediate"}),
        AgentRequest(agent_id="reputation_tracker", action="leaderboard", params={"limit": 5}),
    ]
    return await execute_swarm(SwarmRequest(agents=test_requests))
