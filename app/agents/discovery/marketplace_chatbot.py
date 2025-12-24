"""
Marketplace Discovery Chatbot Agent

Conversational strain discovery using HyperGraphRAG.
Helps users find genetics matching their preferences.

Part of Discovery Agents.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum
import logging

from pydantic import BaseModel, Field

from ..base import (
    AgentRole,
    AgentContext,
    AgentResult,
    BaseAgent,
    AgentRegistry,
)
from ...gamification import gamification_engine

logger = logging.getLogger(__name__)


# Pydantic models for structured I/O
class UserPreferences(BaseModel):
    """User's strain preferences"""
    effects_desired: List[str] = Field(default_factory=list, description="Desired effects like 'relaxing', 'energetic'")
    flavor_profiles: List[str] = Field(default_factory=list, description="Flavor preferences like 'citrus', 'earthy'")
    thc_range: Optional[tuple] = Field(default=None, description="THC percentage range (min, max)")
    cbd_range: Optional[tuple] = Field(default=None, description="CBD percentage range (min, max)")
    grow_difficulty: Optional[str] = Field(default=None, description="'easy', 'moderate', 'advanced'")
    flower_time_max: Optional[int] = Field(default=None, description="Max flower time in days")
    autoflower: Optional[bool] = Field(default=None, description="Preference for autoflowers")
    indoor_outdoor: Optional[str] = Field(default=None, description="'indoor', 'outdoor', 'both'")


class StrainMatch(BaseModel):
    """A matched strain result"""
    id: int
    name: str
    breeder: str
    match_score: float = Field(ge=0, le=1, description="How well strain matches preferences")
    genetics_type: str
    thc_percent: float
    flower_time_days: int
    effects: List[str]
    flavors: List[str]
    match_reasons: List[str]


class SearchQuery(BaseModel):
    """Natural language search query"""
    query: str
    filters: Dict[str, Any] = Field(default_factory=dict)
    limit: int = Field(default=10, ge=1, le=50)


class MarketplaceChatbotAgent(BaseAgent):
    """
    Conversational marketplace discovery agent.
    
    Capabilities:
    - Natural language strain search
    - Preference-based recommendations
    - Terpene profile matching
    - Breeder discovery
    - Price comparisons
    
    Integrates with:
    - HyperGraphRAG for semantic search (planned)
    - Strain database
    - Gamification (XP for discoveries)
    """
    
    def __init__(self):
        super().__init__(
            agent_id="marketplace_chatbot",
            name="Marketplace Discovery Chatbot",
            role=AgentRole.DISCOVERY,
            description="Conversational strain discovery and recommendations",
        )
        
        # Register MCP tools
        self.register_tool(
            "search_strains",
            self.search_strains,
            "Search strains by natural language query"
        )
        self.register_tool(
            "get_recommendations",
            self.get_recommendations,
            "Get personalized strain recommendations"
        )
        self.register_tool(
            "compare_strains",
            self.compare_strains,
            "Compare multiple strains side by side"
        )
        self.register_tool(
            "find_similar",
            self.find_similar,
            "Find strains similar to a given strain"
        )
        
        # Mock strain database (would connect to real DB)
        self._strain_db = self._load_mock_strains()
        
    async def execute(self, context: AgentContext, **kwargs) -> AgentResult:
        """Execute marketplace discovery"""
        action = kwargs.get("action", "search")
        
        try:
            if action == "search":
                query = SearchQuery(
                    query=kwargs.get("query", ""),
                    filters=kwargs.get("filters", {}),
                    limit=kwargs.get("limit", 10),
                )
                result = await self.search_strains(query)
            elif action == "recommend":
                prefs = UserPreferences(**kwargs.get("preferences", {}))
                result = await self.get_recommendations(prefs)
            elif action == "compare":
                result = await self.compare_strains(
                    strain_ids=kwargs.get("strain_ids", [])
                )
            elif action == "similar":
                result = await self.find_similar(
                    strain_id=kwargs.get("strain_id"),
                    limit=kwargs.get("limit", 5),
                )
            else:
                result = {"error": f"Unknown action: {action}"}
                
            # Award XP for discovery
            if context.user_id:
                gamification_engine.award_xp(
                    context.user_id, 5, "marketplace_discovery"
                )
                
            return AgentResult(
                success=True,
                agent_id=self.agent_id,
                output=result,
                confidence=0.85,
                xp_reward=5,
                next_actions=["view_details", "add_to_wishlist", "compare"],
            )
            
        except Exception as e:
            logger.error(f"MarketplaceChatbot error: {e}")
            return AgentResult(
                success=False,
                agent_id=self.agent_id,
                output=None,
                error=str(e),
            )
    
    async def search_strains(self, query: SearchQuery) -> Dict[str, Any]:
        """
        Search strains using natural language.
        
        Parses query for intent and filters.
        Would integrate with HyperGraphRAG for semantic search.
        """
        search_terms = query.query.lower().split()
        
        # Parse common patterns
        parsed_filters = self._parse_query(query.query)
        merged_filters = {**parsed_filters, **query.filters}
        
        # Filter strains
        matches = []
        for strain in self._strain_db:
            score = self._calculate_match_score(strain, search_terms, merged_filters)
            if score > 0.3:
                matches.append({
                    **strain,
                    "match_score": round(score, 2),
                    "match_reasons": self._get_match_reasons(strain, search_terms, merged_filters),
                })
                
        # Sort by score and limit
        matches.sort(key=lambda x: x["match_score"], reverse=True)
        matches = matches[:query.limit]
        
        return {
            "query": query.query,
            "parsed_intent": parsed_filters,
            "total_matches": len(matches),
            "results": matches,
            "suggestions": self._get_search_suggestions(search_terms),
        }
    
    async def get_recommendations(self, preferences: UserPreferences) -> Dict[str, Any]:
        """Get personalized recommendations based on preferences"""
        recommendations = []
        
        for strain in self._strain_db:
            score = self._score_preferences(strain, preferences)
            if score > 0.5:
                recommendations.append({
                    **strain,
                    "match_score": round(score, 2),
                    "match_reasons": self._get_preference_matches(strain, preferences),
                })
                
        recommendations.sort(key=lambda x: x["match_score"], reverse=True)
        
        return {
            "preferences_summary": preferences.dict(exclude_none=True),
            "total_matches": len(recommendations),
            "top_recommendations": recommendations[:10],
            "tip": self._get_recommendation_tip(preferences),
        }
    
    async def compare_strains(self, strain_ids: List[int]) -> Dict[str, Any]:
        """Compare multiple strains side by side"""
        if len(strain_ids) < 2:
            return {"error": "Need at least 2 strains to compare"}
            
        strains = [s for s in self._strain_db if s["id"] in strain_ids]
        
        if len(strains) < 2:
            return {"error": "Could not find all requested strains"}
            
        comparison = {
            "strains": strains,
            "comparison_table": {
                "thc": {s["name"]: s["thc_percent"] for s in strains},
                "flower_time": {s["name"]: s["flower_time_days"] for s in strains},
                "difficulty": {s["name"]: s["difficulty"] for s in strains},
                "effects": {s["name"]: s["effects"] for s in strains},
            },
            "winner_categories": self._determine_winners(strains),
            "recommendation": self._compare_recommendation(strains),
        }
        
        return comparison
    
    async def find_similar(self, strain_id: int, limit: int = 5) -> Dict[str, Any]:
        """Find strains similar to a given strain"""
        target = next((s for s in self._strain_db if s["id"] == strain_id), None)
        
        if not target:
            return {"error": f"Strain {strain_id} not found"}
            
        similar = []
        for strain in self._strain_db:
            if strain["id"] == strain_id:
                continue
            similarity = self._calculate_similarity(target, strain)
            if similarity > 0.5:
                similar.append({
                    **strain,
                    "similarity_score": round(similarity, 2),
                    "similar_because": self._get_similarity_reasons(target, strain),
                })
                
        similar.sort(key=lambda x: x["similarity_score"], reverse=True)
        
        return {
            "target_strain": target["name"],
            "similar_strains": similar[:limit],
        }
    
    def _load_mock_strains(self) -> List[Dict]:
        """Load mock strain database"""
        return [
            {
                "id": 1,
                "name": "Blue Dream",
                "breeder": "DJ Short",
                "genetics_type": "hybrid",
                "thc_percent": 21.0,
                "cbd_percent": 0.1,
                "flower_time_days": 60,
                "difficulty": "easy",
                "effects": ["relaxed", "happy", "euphoric", "creative"],
                "flavors": ["blueberry", "sweet", "earthy"],
                "terpenes": {"myrcene": 0.5, "pinene": 0.3, "caryophyllene": 0.2},
                "yield_indoor": "medium-high",
                "autoflower": False,
            },
            {
                "id": 2,
                "name": "Girl Scout Cookies",
                "breeder": "Cookie Fam",
                "genetics_type": "hybrid",
                "thc_percent": 25.0,
                "cbd_percent": 0.1,
                "flower_time_days": 63,
                "difficulty": "moderate",
                "effects": ["euphoric", "relaxed", "happy", "uplifted"],
                "flavors": ["sweet", "earthy", "pungent"],
                "terpenes": {"caryophyllene": 0.4, "limonene": 0.3, "humulene": 0.2},
                "yield_indoor": "medium",
                "autoflower": False,
            },
            {
                "id": 3,
                "name": "Northern Lights",
                "breeder": "Sensi Seeds",
                "genetics_type": "indica",
                "thc_percent": 18.0,
                "cbd_percent": 0.1,
                "flower_time_days": 50,
                "difficulty": "easy",
                "effects": ["relaxed", "sleepy", "happy", "euphoric"],
                "flavors": ["earthy", "pine", "sweet"],
                "terpenes": {"myrcene": 0.6, "pinene": 0.2, "caryophyllene": 0.1},
                "yield_indoor": "high",
                "autoflower": False,
            },
            {
                "id": 4,
                "name": "Sour Diesel",
                "breeder": "Unknown",
                "genetics_type": "sativa",
                "thc_percent": 22.0,
                "cbd_percent": 0.2,
                "flower_time_days": 77,
                "difficulty": "moderate",
                "effects": ["energetic", "happy", "uplifted", "creative"],
                "flavors": ["diesel", "pungent", "earthy"],
                "terpenes": {"caryophyllene": 0.4, "myrcene": 0.3, "limonene": 0.3},
                "yield_indoor": "medium",
                "autoflower": False,
            },
            {
                "id": 5,
                "name": "Gorilla Glue #4",
                "breeder": "GG Strains",
                "genetics_type": "hybrid",
                "thc_percent": 28.0,
                "cbd_percent": 0.1,
                "flower_time_days": 63,
                "difficulty": "moderate",
                "effects": ["relaxed", "euphoric", "happy", "uplifted"],
                "flavors": ["earthy", "pine", "pungent"],
                "terpenes": {"caryophyllene": 0.5, "limonene": 0.2, "myrcene": 0.2},
                "yield_indoor": "high",
                "autoflower": False,
            },
        ]
    
    def _parse_query(self, query: str) -> Dict[str, Any]:
        """Parse natural language query for filters"""
        query_lower = query.lower()
        filters = {}
        
        # Detect genetics type
        if "indica" in query_lower:
            filters["genetics_type"] = "indica"
        elif "sativa" in query_lower:
            filters["genetics_type"] = "sativa"
        elif "hybrid" in query_lower:
            filters["genetics_type"] = "hybrid"
            
        # Detect difficulty
        if "easy" in query_lower or "beginner" in query_lower:
            filters["difficulty"] = "easy"
        elif "advanced" in query_lower or "expert" in query_lower:
            filters["difficulty"] = "advanced"
            
        # Detect effects
        effect_keywords = ["relaxing", "energetic", "creative", "sleepy", "happy", "euphoric"]
        for effect in effect_keywords:
            if effect in query_lower:
                filters.setdefault("effects", []).append(effect.replace("ing", "ed"))
                
        # Detect high THC
        if "high thc" in query_lower or "potent" in query_lower or "strong" in query_lower:
            filters["min_thc"] = 25
            
        return filters
    
    def _calculate_match_score(
        self, 
        strain: Dict, 
        terms: List[str], 
        filters: Dict
    ) -> float:
        """Calculate how well strain matches search"""
        score = 0.0
        max_score = 1.0
        
        # Name match
        name_lower = strain["name"].lower()
        for term in terms:
            if term in name_lower:
                score += 0.4
                
        # Breeder match
        if strain["breeder"].lower() in " ".join(terms):
            score += 0.3
            
        # Genetics type filter
        if "genetics_type" in filters:
            if strain["genetics_type"] == filters["genetics_type"]:
                score += 0.2
                
        # Effects filter
        if "effects" in filters:
            matching_effects = set(filters["effects"]) & set(strain["effects"])
            score += len(matching_effects) * 0.1
            
        # Difficulty filter
        if "difficulty" in filters:
            if strain["difficulty"] == filters["difficulty"]:
                score += 0.1
                
        # THC filter
        if "min_thc" in filters:
            if strain["thc_percent"] >= filters["min_thc"]:
                score += 0.2
                
        return min(score, max_score)
    
    def _score_preferences(self, strain: Dict, prefs: UserPreferences) -> float:
        """Score strain against user preferences"""
        score = 0.5  # Base score
        
        # Effects match
        if prefs.effects_desired:
            matches = set(prefs.effects_desired) & set(strain["effects"])
            score += len(matches) * 0.1
            
        # Flavor match
        if prefs.flavor_profiles:
            matches = set(prefs.flavor_profiles) & set(strain["flavors"])
            score += len(matches) * 0.1
            
        # Difficulty match
        if prefs.grow_difficulty:
            if strain["difficulty"] == prefs.grow_difficulty:
                score += 0.15
                
        # Flower time
        if prefs.flower_time_max:
            if strain["flower_time_days"] <= prefs.flower_time_max:
                score += 0.1
                
        return min(score, 1.0)
    
    def _get_match_reasons(self, strain: Dict, terms: List[str], filters: Dict) -> List[str]:
        """Get reasons why strain matched"""
        reasons = []
        
        name_lower = strain["name"].lower()
        for term in terms:
            if term in name_lower:
                reasons.append(f"Name matches '{term}'")
                
        if "genetics_type" in filters and strain["genetics_type"] == filters["genetics_type"]:
            reasons.append(f"Is {filters['genetics_type']}")
            
        if "effects" in filters:
            for effect in filters["effects"]:
                if effect in strain["effects"]:
                    reasons.append(f"Provides {effect} effect")
                    
        return reasons if reasons else ["General relevance"]
    
    def _get_preference_matches(self, strain: Dict, prefs: UserPreferences) -> List[str]:
        """Get reasons why strain matches preferences"""
        reasons = []
        
        if prefs.effects_desired:
            for effect in prefs.effects_desired:
                if effect in strain["effects"]:
                    reasons.append(f"✓ {effect.title()} effect")
                    
        if prefs.grow_difficulty and strain["difficulty"] == prefs.grow_difficulty:
            reasons.append(f"✓ {prefs.grow_difficulty.title()} difficulty")
            
        return reasons
    
    def _get_search_suggestions(self, terms: List[str]) -> List[str]:
        """Get related search suggestions"""
        return [
            "Try adding 'indica' or 'sativa' for type",
            "Add 'high thc' for potent strains",
            "Include effects like 'relaxing' or 'energetic'",
        ]
    
    def _get_recommendation_tip(self, prefs: UserPreferences) -> str:
        """Get contextual tip"""
        if prefs.grow_difficulty == "easy":
            return "Great choice for beginners! These strains are forgiving and resilient."
        return "These strains match your preferences - check reviews for more details."
    
    def _calculate_similarity(self, strain1: Dict, strain2: Dict) -> float:
        """Calculate similarity between two strains"""
        score = 0.0
        
        # Same genetics type
        if strain1["genetics_type"] == strain2["genetics_type"]:
            score += 0.3
            
        # Overlapping effects
        effect_overlap = set(strain1["effects"]) & set(strain2["effects"])
        score += len(effect_overlap) * 0.1
        
        # Similar THC
        thc_diff = abs(strain1["thc_percent"] - strain2["thc_percent"])
        if thc_diff < 3:
            score += 0.2
            
        # Similar flower time
        time_diff = abs(strain1["flower_time_days"] - strain2["flower_time_days"])
        if time_diff < 7:
            score += 0.15
            
        return min(score, 1.0)
    
    def _get_similarity_reasons(self, target: Dict, similar: Dict) -> List[str]:
        """Get reasons for similarity"""
        reasons = []
        
        if target["genetics_type"] == similar["genetics_type"]:
            reasons.append(f"Both are {target['genetics_type']}")
            
        common_effects = set(target["effects"]) & set(similar["effects"])
        if common_effects:
            reasons.append(f"Shared effects: {', '.join(list(common_effects)[:2])}")
            
        return reasons
    
    def _determine_winners(self, strains: List[Dict]) -> Dict[str, str]:
        """Determine winner in each category"""
        return {
            "highest_thc": max(strains, key=lambda s: s["thc_percent"])["name"],
            "fastest_flower": min(strains, key=lambda s: s["flower_time_days"])["name"],
            "easiest_grow": next((s["name"] for s in strains if s["difficulty"] == "easy"), strains[0]["name"]),
        }
    
    def _compare_recommendation(self, strains: List[Dict]) -> str:
        """Generate comparison recommendation"""
        easiest = min(strains, key=lambda s: {"easy": 1, "moderate": 2, "advanced": 3}.get(s["difficulty"], 2))
        return f"For beginners, {easiest['name']} is recommended due to its {easiest['difficulty']} difficulty."


# Register agent
AgentRegistry.register(MarketplaceChatbotAgent())
