"""
CultivAR Agent MCP Server

Exposes all agent tools via Model Context Protocol (MCP).
Enables AI systems to interact with CultivAR agents.

Integrates:
- All registered agents from AgentRegistry
- Swarm execution for parallel agent workflows
- EvoAgentX metrics for performance tracking
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional
from dataclasses import asdict
import json

logger = logging.getLogger(__name__)


# Import agents to register them
from ..agents import AgentRegistry, AgentContext, SwarmExecutor, AgentRole
from ..agents.discovery import StrainSommelierAgent
from ..agents.growing import PlantHealthVisionAgent, DailyCheckInAgent
from ..gamification import gamification_engine


class CultivARAgentMCPServer:
    """
    MCP Server for CultivAR Agent Ecosystem.
    
    Provides tools for:
    - Individual agent execution
    - Swarm (parallel) agent execution
    - Gamification interactions
    - Agent performance metrics
    """
    
    def __init__(self):
        self.name = "cultivar-agents"
        self.version = "1.0.0"
        self._tools = self._build_tool_list()
        
    def _build_tool_list(self) -> List[Dict[str, Any]]:
        """Build list of available MCP tools"""
        tools = []
        
        # Core agent tools
        tools.extend([
            {
                "name": "list_agents",
                "description": "List all available CultivAR agents",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "role": {
                            "type": "string",
                            "description": "Filter by role (discovery, growing, harvest, etc.)",
                            "enum": ["discovery", "planning", "growing", "harvest", "community", "marketing"],
                        },
                    },
                },
            },
            {
                "name": "execute_agent",
                "description": "Execute a specific agent with given context",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "agent_id": {
                            "type": "string",
                            "description": "ID of the agent to execute",
                        },
                        "user_id": {
                            "type": "integer",
                            "description": "User ID for context",
                        },
                        "action": {
                            "type": "string",
                            "description": "Action to perform",
                        },
                        "params": {
                            "type": "object",
                            "description": "Additional parameters for the agent",
                        },
                    },
                    "required": ["agent_id", "user_id"],
                },
            },
            {
                "name": "execute_swarm",
                "description": "Execute multiple agents in parallel (swarm pattern)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "role": {
                            "type": "string",
                            "description": "Role of agents to include in swarm",
                        },
                        "user_id": {
                            "type": "integer",
                            "description": "User ID for context",
                        },
                        "consensus": {
                            "type": "boolean",
                            "description": "Use hive-mind consensus mode",
                            "default": False,
                        },
                    },
                    "required": ["role", "user_id"],
                },
            },
        ])
        
        # Discovery agent tools
        tools.extend([
            {
                "name": "optimize_flower_batches",
                "description": "Group strains by similar flower times for batch growing",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "strains": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "flower_time_days": {"type": "integer"},
                                },
                            },
                            "description": "List of strains with flower times",
                        },
                    },
                    "required": ["strains"],
                },
            },
            {
                "name": "recommend_strain_pairing",
                "description": "Get strain pairing recommendations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "preferences": {
                            "type": "object",
                            "description": "User preferences (effects, THC level, etc.)",
                        },
                        "existing_collection": {
                            "type": "array",
                            "items": {"type": "object"},
                            "description": "User's existing strain collection",
                        },
                    },
                },
            },
        ])
        
        # Growing agent tools
        tools.extend([
            {
                "name": "analyze_plant_health",
                "description": "Analyze plant photo for health issues using AI vision",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "image_data": {
                            "type": "string",
                            "description": "Base64 encoded plant photo",
                        },
                        "plant_id": {
                            "type": "integer",
                            "description": "ID of the plant",
                        },
                        "growth_stage": {
                            "type": "string",
                            "enum": ["seedling", "vegetative", "flowering", "harvest"],
                            "description": "Current growth stage",
                        },
                    },
                    "required": ["image_data"],
                },
            },
            {
                "name": "daily_checkin",
                "description": "Perform daily check-in with XP rewards",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "User ID",
                        },
                        "observations": {
                            "type": "object",
                            "description": "Plant observations keyed by plant_id",
                        },
                        "photos_uploaded": {
                            "type": "integer",
                            "description": "Number of photos uploaded",
                        },
                        "environment_logged": {
                            "type": "boolean",
                            "description": "Whether environment was logged",
                        },
                    },
                    "required": ["user_id"],
                },
            },
            {
                "name": "get_streak_status",
                "description": "Get user's current check-in streak status",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "User ID",
                        },
                    },
                    "required": ["user_id"],
                },
            },
        ])
        
        # Gamification tools
        tools.extend([
            {
                "name": "get_user_progress",
                "description": "Get user's gamification progress (XP, level, achievements)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "User ID",
                        },
                    },
                    "required": ["user_id"],
                },
            },
            {
                "name": "award_xp",
                "description": "Award XP to a user",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer"},
                        "amount": {"type": "integer"},
                        "source": {"type": "string"},
                    },
                    "required": ["user_id", "amount", "source"],
                },
            },
            {
                "name": "check_achievements",
                "description": "Check if user qualifies for achievements",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer"},
                        "metrics": {
                            "type": "object",
                            "description": "User metrics to check against achievements",
                        },
                    },
                    "required": ["user_id", "metrics"],
                },
            },
            {
                "name": "get_leaderboard",
                "description": "Get XP leaderboard",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "default": 10,
                        },
                    },
                },
            },
        ])
        
        # Agent metrics tools (EvoAgentX)
        tools.extend([
            {
                "name": "get_agent_metrics",
                "description": "Get performance metrics for an agent (EvoAgentX)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "agent_id": {"type": "string"},
                    },
                    "required": ["agent_id"],
                },
            },
            {
                "name": "record_agent_feedback",
                "description": "Record user feedback for agent evolution",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "agent_id": {"type": "string"},
                        "positive": {"type": "boolean"},
                    },
                    "required": ["agent_id", "positive"],
                },
            },
        ])
        
        return tools
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Return list of available tools"""
        return self._tools
    
    async def execute_tool(
        self, 
        tool_name: str, 
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a tool by name"""
        
        handlers = {
            "list_agents": self._list_agents,
            "execute_agent": self._execute_agent,
            "execute_swarm": self._execute_swarm,
            "optimize_flower_batches": self._optimize_flower_batches,
            "recommend_strain_pairing": self._recommend_strain_pairing,
            "analyze_plant_health": self._analyze_plant_health,
            "daily_checkin": self._daily_checkin,
            "get_streak_status": self._get_streak_status,
            "get_user_progress": self._get_user_progress,
            "award_xp": self._award_xp,
            "check_achievements": self._check_achievements,
            "get_leaderboard": self._get_leaderboard,
            "get_agent_metrics": self._get_agent_metrics,
            "record_agent_feedback": self._record_agent_feedback,
        }
        
        handler = handlers.get(tool_name)
        if not handler:
            return {"error": f"Unknown tool: {tool_name}"}
            
        try:
            return await handler(arguments)
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            return {"error": str(e)}
    
    # Tool handlers
    
    async def _list_agents(self, args: Dict) -> Dict:
        """List available agents"""
        role_filter = args.get("role")
        
        if role_filter:
            try:
                role = AgentRole(role_filter)
                agents = AgentRegistry.get_by_role(role)
            except ValueError:
                return {"error": f"Invalid role: {role_filter}"}
        else:
            agents = AgentRegistry.get_all()
            
        return {
            "agents": [
                {
                    "id": a.agent_id,
                    "name": a.name,
                    "role": a.role.value,
                    "description": a.description,
                }
                for a in agents
            ],
            "count": len(agents),
        }
    
    async def _execute_agent(self, args: Dict) -> Dict:
        """Execute specific agent"""
        agent_id = args["agent_id"]
        user_id = args["user_id"]
        
        agent = AgentRegistry.get(agent_id)
        if not agent:
            return {"error": f"Agent not found: {agent_id}"}
            
        context = AgentContext(
            user_id=user_id,
            session_id=f"mcp-{user_id}",
            metadata=args.get("params", {}),
        )
        
        result = await agent.execute(
            context, 
            action=args.get("action"),
            **args.get("params", {}),
        )
        
        return {
            "success": result.success,
            "agent_id": result.agent_id,
            "output": result.output,
            "confidence": result.confidence,
            "xp_reward": result.xp_reward,
            "next_actions": result.next_actions,
        }
    
    async def _execute_swarm(self, args: Dict) -> Dict:
        """Execute swarm of agents"""
        role = AgentRole(args["role"])
        user_id = args["user_id"]
        use_consensus = args.get("consensus", False)
        
        swarm = AgentRegistry.create_swarm(role)
        context = AgentContext(
            user_id=user_id,
            session_id=f"swarm-{user_id}",
        )
        
        if use_consensus:
            result = await swarm.execute_with_consensus(context)
            return {
                "mode": "consensus",
                "success": result.success,
                "output": result.output,
                "confidence": result.confidence,
            }
        else:
            results = await swarm.execute_all(context)
            return {
                "mode": "parallel",
                "results": [
                    {
                        "agent_id": r.agent_id,
                        "success": r.success,
                        "output": r.output,
                    }
                    for r in results
                ],
            }
    
    async def _optimize_flower_batches(self, args: Dict) -> Dict:
        """Optimize flower time batches"""
        agent = AgentRegistry.get("strain_sommelier")
        if not agent:
            return {"error": "Strain Sommelier agent not available"}
            
        return await agent.optimize_flower_batches(args.get("strains", []))
    
    async def _recommend_strain_pairing(self, args: Dict) -> Dict:
        """Get strain pairing recommendations"""
        agent = AgentRegistry.get("strain_sommelier")
        if not agent:
            return {"error": "Strain Sommelier agent not available"}
            
        return await agent.recommend_pairing(
            user_preferences=args.get("preferences", {}),
            existing_collection=args.get("existing_collection", []),
        )
    
    async def _analyze_plant_health(self, args: Dict) -> Dict:
        """Analyze plant health from photo"""
        agent = AgentRegistry.get("plant_health_vision")
        if not agent:
            return {"error": "Plant Health Vision agent not available"}
            
        return await agent.analyze_plant_photo(
            image_data=args.get("image_data", ""),
            plant_id=args.get("plant_id"),
            growth_stage=args.get("growth_stage", "vegetative"),
        )
    
    async def _daily_checkin(self, args: Dict) -> Dict:
        """Process daily check-in"""
        agent = AgentRegistry.get("daily_checkin")
        if not agent:
            return {"error": "Daily Check-In agent not available"}
            
        return await agent.submit_checkin(
            user_id=args["user_id"],
            checkin_data={
                "observations": args.get("observations", {}),
                "photos_uploaded": args.get("photos_uploaded", 0),
                "environment_logged": args.get("environment_logged", False),
            },
        )
    
    async def _get_streak_status(self, args: Dict) -> Dict:
        """Get streak status"""
        agent = AgentRegistry.get("daily_checkin")
        if not agent:
            return {"error": "Daily Check-In agent not available"}
            
        return await agent.get_streak_status(args["user_id"])
    
    async def _get_user_progress(self, args: Dict) -> Dict:
        """Get user gamification progress"""
        progress = gamification_engine.get_user_progress(args["user_id"])
        return {
            "user_id": progress.user_id,
            "total_xp": progress.total_xp,
            "level": progress.level,
            "level_progress": progress.level_progress_percent,
            "xp_for_next_level": progress.xp_for_next_level,
            "current_streak": progress.current_streak,
            "longest_streak": progress.longest_streak,
            "achievements": progress.achievements,
            "discount": gamification_engine.get_user_discount(args["user_id"]),
        }
    
    async def _award_xp(self, args: Dict) -> Dict:
        """Award XP to user"""
        return gamification_engine.award_xp(
            user_id=args["user_id"],
            amount=args["amount"],
            source=args["source"],
        )
    
    async def _check_achievements(self, args: Dict) -> Dict:
        """Check achievements"""
        unlocked = gamification_engine.check_achievements(
            user_id=args["user_id"],
            metrics=args.get("metrics", {}),
        )
        return {"achievements_unlocked": unlocked}
    
    async def _get_leaderboard(self, args: Dict) -> Dict:
        """Get leaderboard"""
        return {
            "leaderboard": gamification_engine.get_leaderboard(
                limit=args.get("limit", 10)
            )
        }
    
    async def _get_agent_metrics(self, args: Dict) -> Dict:
        """Get agent performance metrics"""
        agent = AgentRegistry.get(args["agent_id"])
        if not agent:
            return {"error": f"Agent not found: {args['agent_id']}"}
            
        metrics = agent.metrics
        return {
            "agent_id": metrics.agent_id,
            "total_executions": metrics.total_executions,
            "success_rate": metrics.success_rate,
            "feedback_score": metrics.feedback_score,
            "avg_confidence": metrics.avg_confidence,
            "outcome_accuracy": metrics.outcome_accuracy,
        }
    
    async def _record_agent_feedback(self, args: Dict) -> Dict:
        """Record agent feedback"""
        agent = AgentRegistry.get(args["agent_id"])
        if not agent:
            return {"error": f"Agent not found: {args['agent_id']}"}
            
        agent.record_feedback(args["positive"])
        return {
            "recorded": True,
            "new_feedback_score": agent.metrics.feedback_score,
        }


# Singleton instance
cultivar_agent_mcp = CultivARAgentMCPServer()
