"""
Strain Sommelier Agent

Expert pairing and flower time optimization.
Groups similar cycle lengths for efficient batch growing.

Part of Discovery Agents.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import logging

from ..base import (
    AgentRole,
    AgentContext,
    AgentResult,
    BaseAgent,
    AgentRegistry,
)

logger = logging.getLogger(__name__)


@dataclass
class StrainProfile:
    """Strain data for sommelier recommendations"""
    id: int
    name: str
    breeder: str
    flower_time_days: int
    genetics_type: str  # indica, sativa, hybrid
    thc_percent: float
    cbd_percent: float
    terpene_profile: Dict[str, float]
    difficulty: str  # easy, moderate, advanced
    yield_indoor: str
    effects: List[str]


@dataclass
class BatchRecommendation:
    """Recommendation for batch growing"""
    batch_name: str
    strains: List[StrainProfile]
    avg_flower_time: float
    flower_time_range: str
    notes: str
    compatibility_score: float


class StrainSommelierAgent(BaseAgent):
    """
    Expert strain pairing and flower time optimization.
    
    Capabilities:
    - Group strains by similar flower times for batch growing
    - Recommend pairings based on terpene profiles
    - Suggest strains based on user preferences
    - Optimize grow room scheduling
    """
    
    def __init__(self):
        super().__init__(
            agent_id="strain_sommelier",
            name="Strain Sommelier",
            role=AgentRole.DISCOVERY,
            description="Expert strain pairing and flower time optimization",
        )
        
        # Register MCP tools
        self.register_tool(
            "optimize_flower_batches",
            self.optimize_flower_batches,
            "Group strains by similar flower times for batch growing"
        )
        self.register_tool(
            "recommend_pairing",
            self.recommend_pairing,
            "Recommend strain pairings based on preferences"
        )
        self.register_tool(
            "analyze_terpene_match",
            self.analyze_terpene_match,
            "Find strains with similar terpene profiles"
        )
        
    async def execute(self, context: AgentContext, **kwargs) -> AgentResult:
        """Execute sommelier recommendations"""
        action = kwargs.get("action", "recommend")
        
        try:
            if action == "optimize_batches":
                result = await self.optimize_flower_batches(
                    context.metadata.get("strains", [])
                )
            elif action == "recommend":
                result = await self.recommend_pairing(
                    user_preferences=context.metadata.get("preferences", {}),
                    existing_collection=context.metadata.get("collection", []),
                )
            else:
                result = {"error": f"Unknown action: {action}"}
                
            self.record_execution(AgentResult(
                success=True,
                agent_id=self.agent_id,
                output=result,
                confidence=0.85,
                xp_reward=5,
            ))
            
            return AgentResult(
                success=True,
                agent_id=self.agent_id,
                output=result,
                confidence=0.85,
                xp_reward=5,
                next_actions=["view_strain_details", "add_to_collection"],
            )
            
        except Exception as e:
            logger.error(f"StrainSommelier error: {e}")
            return AgentResult(
                success=False,
                agent_id=self.agent_id,
                output=None,
                error=str(e),
            )
    
    async def optimize_flower_batches(
        self, 
        strains: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Group strains by similar flower times.
        
        Example output:
        ```
        User's genetics (by flower time):
        ├── Blue Dream (60 days)      ─┐
        ├── GSC (58 days)              │ → "Run together - similar timing"
        ├── Zkittlez (63 days)        ─┘
        ├── Purple Punch (70 days)    ─── "Good for next batch"
        └── Durban Poison (120 days)  ─── "Save for dedicated long run"
        ```
        """
        if not strains:
            return {"batches": [], "message": "No strains provided"}
            
        # Sort by flower time
        sorted_strains = sorted(
            strains, 
            key=lambda s: s.get("flower_time_days", 60)
        )
        
        # Group into batches (within 7 days of each other)
        batches = []
        current_batch = []
        batch_start_time = None
        
        for strain in sorted_strains:
            flower_time = strain.get("flower_time_days", 60)
            
            if batch_start_time is None:
                batch_start_time = flower_time
                current_batch = [strain]
            elif flower_time - batch_start_time <= 7:
                current_batch.append(strain)
            else:
                # Finalize current batch
                if current_batch:
                    batches.append(self._create_batch(current_batch, len(batches) + 1))
                # Start new batch
                batch_start_time = flower_time
                current_batch = [strain]
                
        # Don't forget last batch
        if current_batch:
            batches.append(self._create_batch(current_batch, len(batches) + 1))
            
        # Generate recommendations
        recommendations = self._generate_batch_recommendations(batches)
        
        return {
            "total_strains": len(strains),
            "num_batches": len(batches),
            "batches": batches,
            "recommendations": recommendations,
            "timeline_ascii": self._generate_timeline_ascii(batches),
        }
    
    async def recommend_pairing(
        self,
        user_preferences: Dict[str, Any],
        existing_collection: List[Dict] = None,
    ) -> Dict[str, Any]:
        """Recommend strain pairings based on preferences"""
        
        # Mock recommendations for now - would integrate with HyperGraphRAG
        recommendations = [
            {
                "strain": "Wedding Cake",
                "reason": "Matches your indica preference with high THC",
                "compatibility": 0.92,
                "flower_time": 56,
                "pairs_well_with": ["Gelato", "Purple Punch"],
            },
            {
                "strain": "Blue Dream",
                "reason": "Balanced hybrid, great for daytime",
                "compatibility": 0.88,
                "flower_time": 60,
                "pairs_well_with": ["GSC", "Zkittlez"],
            },
        ]
        
        return {
            "recommendations": recommendations,
            "based_on": user_preferences,
            "collection_size": len(existing_collection or []),
        }
    
    async def analyze_terpene_match(
        self,
        target_profile: Dict[str, float],
        candidate_strains: List[Dict],
    ) -> List[Dict[str, Any]]:
        """Find strains with similar terpene profiles"""
        
        matches = []
        for strain in candidate_strains:
            strain_profile = strain.get("terpene_profile", {})
            similarity = self._calculate_terpene_similarity(
                target_profile, 
                strain_profile
            )
            if similarity > 0.7:
                matches.append({
                    "strain": strain.get("name"),
                    "similarity": similarity,
                    "dominant_terpenes": list(strain_profile.keys())[:3],
                })
                
        return sorted(matches, key=lambda x: x["similarity"], reverse=True)
    
    def _create_batch(self, strains: List[Dict], batch_num: int) -> Dict[str, Any]:
        """Create a batch recommendation"""
        flower_times = [s.get("flower_time_days", 60) for s in strains]
        avg_time = sum(flower_times) / len(flower_times)
        
        return {
            "batch_number": batch_num,
            "strains": [s.get("name", "Unknown") for s in strains],
            "strain_count": len(strains),
            "avg_flower_time": round(avg_time, 1),
            "min_flower_time": min(flower_times),
            "max_flower_time": max(flower_times),
            "range": f"{min(flower_times)}-{max(flower_times)} days",
        }
    
    def _generate_batch_recommendations(self, batches: List[Dict]) -> List[str]:
        """Generate human-readable recommendations"""
        recommendations = []
        
        for i, batch in enumerate(batches):
            if batch["strain_count"] > 1:
                names = ", ".join(batch["strains"][:3])
                if len(batch["strains"]) > 3:
                    names += f" (+{len(batch['strains']) - 3} more)"
                recommendations.append(
                    f"Batch {i+1}: Run {names} together - similar timing ({batch['range']})"
                )
            else:
                strain = batch["strains"][0]
                time = batch["avg_flower_time"]
                if time > 90:
                    recommendations.append(
                        f"{strain} ({int(time)} days): Save for dedicated long run"
                    )
                else:
                    recommendations.append(
                        f"{strain} ({int(time)} days): Can run solo or wait for matching strain"
                    )
                    
        return recommendations
    
    def _generate_timeline_ascii(self, batches: List[Dict]) -> str:
        """Generate ASCII timeline visualization"""
        lines = ["Flower Time Batches:"]
        
        for batch in batches:
            for strain in batch["strains"]:
                time = batch["avg_flower_time"]
                bar_length = int(time / 5)  # Scale
                bar = "█" * bar_length
                lines.append(f"├── {strain} ({int(time)}d) {bar}")
                
        return "\n".join(lines)
    
    def _calculate_terpene_similarity(
        self, 
        profile1: Dict[str, float], 
        profile2: Dict[str, float]
    ) -> float:
        """Calculate cosine similarity between terpene profiles"""
        all_terpenes = set(profile1.keys()) | set(profile2.keys())
        
        if not all_terpenes:
            return 0.0
            
        vec1 = [profile1.get(t, 0) for t in all_terpenes]
        vec2 = [profile2.get(t, 0) for t in all_terpenes]
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        mag1 = sum(a ** 2 for a in vec1) ** 0.5
        mag2 = sum(b ** 2 for b in vec2) ** 0.5
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
            
        return dot_product / (mag1 * mag2)


# Register agent
AgentRegistry.register(StrainSommelierAgent())
