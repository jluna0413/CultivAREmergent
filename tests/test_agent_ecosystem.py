"""
Tests for CultivAR Agent Ecosystem

Tests cover:
- Agent registration and discovery
- Gamification engine
- Swarm execution
- MCP tool integration
"""

import pytest
import asyncio
from app.agents import (
    AgentRegistry,
    AgentRole,
    AgentContext,
    AgentResult,
    SwarmExecutor,
    EvolutionExecutor,
    SequentialThinkingExecutor,
)
from app.agents.discovery import StrainSommelierAgent
from app.agents.growing import PlantHealthVisionAgent, DailyCheckInAgent
from app.gamification import gamification_engine, ACHIEVEMENTS


class TestAgentRegistry:
    """Test agent registration and discovery"""
    
    def test_agents_registered(self):
        """All agents should be registered"""
        agents = AgentRegistry.get_all()
        assert len(agents) >= 3
        
        agent_ids = [a.agent_id for a in agents]
        assert "strain_sommelier" in agent_ids
        assert "plant_health_vision" in agent_ids
        assert "daily_checkin" in agent_ids
    
    def test_get_by_role(self):
        """Should filter agents by role"""
        discovery = AgentRegistry.get_by_role(AgentRole.DISCOVERY)
        growing = AgentRegistry.get_by_role(AgentRole.GROWING)
        
        assert len(discovery) >= 1
        assert len(growing) >= 2
        
        for agent in discovery:
            assert agent.role == AgentRole.DISCOVERY
            
    def test_get_agent_by_id(self):
        """Should retrieve agent by ID"""
        sommelier = AgentRegistry.get("strain_sommelier")
        assert sommelier is not None
        assert sommelier.name == "Strain Sommelier"
        
        nonexistent = AgentRegistry.get("nonexistent_agent")
        assert nonexistent is None


class TestStrainSommelier:
    """Test Strain Sommelier agent"""
    
    @pytest.mark.asyncio
    async def test_optimize_flower_batches(self):
        """Should group strains by flower time"""
        agent = AgentRegistry.get("strain_sommelier")
        
        strains = [
            {"name": "Blue Dream", "flower_time_days": 60},
            {"name": "GSC", "flower_time_days": 58},
            {"name": "Zkittlez", "flower_time_days": 63},
            {"name": "Purple Punch", "flower_time_days": 70},
            {"name": "Durban Poison", "flower_time_days": 120},
        ]
        
        result = await agent.optimize_flower_batches(strains)
        
        assert result["total_strains"] == 5
        assert result["num_batches"] >= 2
        assert "batches" in result
        assert "recommendations" in result
        
    @pytest.mark.asyncio
    async def test_recommend_pairing(self):
        """Should recommend strain pairings"""
        agent = AgentRegistry.get("strain_sommelier")
        
        result = await agent.recommend_pairing(
            user_preferences={"type": "indica", "thc": "high"},
            existing_collection=[],
        )
        
        assert "recommendations" in result
        assert len(result["recommendations"]) > 0


class TestPlantHealthVision:
    """Test Plant Health Vision agent"""
    
    @pytest.mark.asyncio
    async def test_analyze_plant_photo(self):
        """Should analyze plant photo"""
        agent = AgentRegistry.get("plant_health_vision")
        
        result = await agent.analyze_plant_photo(
            image_data="mock_base64_data",
            plant_id=1,
            growth_stage="flowering",
        )
        
        assert "overall_health_score" in result
        assert "issues" in result
        assert "positive_observations" in result
        assert "recommendations" in result
        
    @pytest.mark.asyncio
    async def test_get_treatment_plan(self):
        """Should return treatment plan"""
        agent = AgentRegistry.get("plant_health_vision")
        
        result = await agent.get_treatment_plan(
            issue_type="nitrogen_deficiency",
            severity="low",
            growth_stage="vegetative",
        )
        
        assert "treatment_plan" in result
        

class TestDailyCheckIn:
    """Test Daily Check-In agent"""
    
    @pytest.mark.asyncio
    async def test_start_checkin(self):
        """Should start check-in session"""
        agent = AgentRegistry.get("daily_checkin")
        
        result = await agent.start_checkin(user_id=1)
        
        assert "plants_to_check" in result
        assert "current_streak" in result
        assert "quick_tips" in result
        
    @pytest.mark.asyncio
    async def test_submit_checkin_awards_xp(self):
        """Should award XP on check-in"""
        agent = AgentRegistry.get("daily_checkin")
        
        result = await agent.submit_checkin(
            user_id=999,  # New user
            checkin_data={
                "observations": {1: "Looking great!"},
                "photos_uploaded": 2,
                "environment_logged": True,
            },
        )
        
        assert result["success"] == True
        assert result["total_xp"] > 0
        assert result["streak"] >= 1


class TestGamificationEngine:
    """Test Gamification Engine"""
    
    def test_user_progress(self):
        """Should track user progress"""
        user_id = 100
        progress = gamification_engine.get_user_progress(user_id)
        
        assert progress.user_id == user_id
        assert progress.level == 1
        assert progress.total_xp == 0
        
    def test_award_xp(self):
        """Should award XP and track level"""
        user_id = 101
        
        result = gamification_engine.award_xp(user_id, 50, "test")
        
        assert result["xp_awarded"] == 50
        assert result["total_xp"] == 50
        assert result["level"] >= 1
        
    def test_level_up(self):
        """Should level up when XP threshold reached"""
        user_id = 102
        
        # Award enough XP to level up (100 for level 2)
        gamification_engine.award_xp(user_id, 100, "test")
        
        progress = gamification_engine.get_user_progress(user_id)
        assert progress.level >= 2
        
    def test_daily_checkin_streak(self):
        """Should track check-in streaks"""
        user_id = 103
        
        result = gamification_engine.daily_checkin(user_id)
        
        assert result["checkin_successful"] == True
        assert result["current_streak"] == 1
        assert result["xp_earned"] > 0
        
    def test_achievements(self):
        """Should have predefined achievements"""
        assert len(ACHIEVEMENTS) >= 10
        assert "first_plant" in ACHIEVEMENTS
        assert "streak_7" in ACHIEVEMENTS
        assert "first_harvest" in ACHIEVEMENTS
        
    def test_unlock_achievement(self):
        """Should unlock achievements"""
        user_id = 104
        
        result = gamification_engine.unlock_achievement(user_id, "first_plant")
        
        assert result is not None
        assert result["achievement_unlocked"] == True
        assert result["xp_awarded"] > 0


class TestSwarmExecutor:
    """Test Swarm execution pattern"""
    
    @pytest.mark.asyncio
    async def test_execute_all(self):
        """Should execute all agents in parallel"""
        growing_agents = AgentRegistry.get_by_role(AgentRole.GROWING)
        swarm = SwarmExecutor(growing_agents)
        
        context = AgentContext(
            user_id=1,
            session_id="test",
        )
        
        results = await swarm.execute_all(context, action="start")
        
        assert len(results) == len(growing_agents)
        

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
