"""
Plant Health Vision Agent

AI-powered plant health analysis using Qwen2-VL.
Detects deficiencies, pests, and stress from photos.

Part of Growing Agents.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from enum import Enum
import logging
import base64

from ..base import (
    AgentRole,
    AgentContext,
    AgentResult,
    BaseAgent,
    AgentRegistry,
)
from ...gamification import gamification_engine

logger = logging.getLogger(__name__)


class HealthIssueType(Enum):
    """Types of plant health issues"""
    NUTRIENT_DEFICIENCY = "nutrient_deficiency"
    NUTRIENT_TOXICITY = "nutrient_toxicity"
    PEST = "pest"
    DISEASE = "disease"
    ENVIRONMENTAL_STRESS = "environmental_stress"
    LIGHT_ISSUE = "light_issue"
    WATER_ISSUE = "water_issue"
    PH_ISSUE = "ph_issue"


class IssueSeverity(Enum):
    """Severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class HealthIssue:
    """Detected health issue"""
    type: HealthIssueType
    name: str
    description: str
    severity: IssueSeverity
    confidence: float
    affected_area: str  # e.g., "lower leaves", "new growth"
    solutions: List[str]
    prevention: List[str]


@dataclass
class HealthAnalysisResult:
    """Complete health analysis result"""
    overall_health_score: float  # 0-100
    issues: List[HealthIssue]
    positive_observations: List[str]
    recommendations: List[str]
    follow_up_days: int


class PlantHealthVisionAgent(BaseAgent):
    """
    AI-powered plant health analysis.
    
    Uses Qwen2-VL for image understanding to detect:
    - Nutrient deficiencies (N, P, K, Ca, Mg, Fe, etc.)
    - Pest infestations (spider mites, thrips, aphids, etc.)
    - Diseases (powdery mildew, bud rot, root rot, etc.)
    - Environmental stress (heat, cold, light burn, etc.)
    
    Integrates with:
    - Gamification: Awards XP for health checks
    - EvoAgentX: Learns from user feedback on diagnoses
    """
    
    def __init__(self):
        super().__init__(
            agent_id="plant_health_vision",
            name="Plant Health Vision",
            role=AgentRole.GROWING,
            description="AI-powered plant health analysis from photos",
        )
        
        # Register MCP tools
        self.register_tool(
            "analyze_plant_photo",
            self.analyze_plant_photo,
            "Analyze a plant photo for health issues"
        )
        self.register_tool(
            "get_treatment_plan",
            self.get_treatment_plan,
            "Get detailed treatment plan for detected issues"
        )
        self.register_tool(
            "compare_health_over_time",
            self.compare_health_over_time,
            "Compare health between multiple photos"
        )
        
        # Issue detection knowledge base
        self._issue_patterns = self._load_issue_patterns()
        
    async def execute(self, context: AgentContext, **kwargs) -> AgentResult:
        """Execute health analysis"""
        image_data = kwargs.get("image_data")
        plant_id = kwargs.get("plant_id") or (
            context.plant_ids[0] if context.plant_ids else None
        )
        
        if not image_data:
            return AgentResult(
                success=False,
                agent_id=self.agent_id,
                output=None,
                error="No image data provided",
            )
        
        try:
            # Perform analysis
            result = await self.analyze_plant_photo(
                image_data=image_data,
                plant_id=plant_id,
                growth_stage=kwargs.get("growth_stage", "flowering"),
            )
            
            # Award XP for using health analysis
            xp_result = gamification_engine.award_xp(
                context.user_id,
                15,
                "plant_health_analysis"
            )
            
            # Check for AI health check achievement
            user_metrics = context.metadata.get("user_metrics", {})
            ai_checks = user_metrics.get("ai_health_checks", 0) + 1
            achievements = gamification_engine.check_achievements(
                context.user_id,
                {"ai_health_checks": ai_checks}
            )
            
            return AgentResult(
                success=True,
                agent_id=self.agent_id,
                output=result,
                confidence=result.get("confidence", 0.8),
                xp_reward=15,
                next_actions=self._suggest_next_actions(result),
                feedback_required=result.get("needs_confirmation", False),
            )
            
        except Exception as e:
            logger.error(f"PlantHealthVision error: {e}")
            return AgentResult(
                success=False,
                agent_id=self.agent_id,
                output=None,
                error=str(e),
            )
    
    async def analyze_plant_photo(
        self,
        image_data: str,  # Base64 encoded image
        plant_id: Optional[int] = None,
        growth_stage: str = "vegetative",
    ) -> Dict[str, Any]:
        """
        Analyze a plant photo for health issues.
        
        Uses fine-tuned Qwen3-VL model for image analysis.
        Falls back to mock responses if model unavailable.
        """
        
        try:
            # Get model loader
            from app.ml.model_loader import get_model_loader
            
            model_loader = get_model_loader()
            
            # Construct analysis prompt
            prompt = self._build_analysis_prompt(growth_stage)
            
            # Run inference
            raw_response = await model_loader.analyze_image(
                image_data=image_data,
                question=prompt,
                max_tokens=512,
            )
            
            # Parse structured response
            analysis = self._parse_model_response(
                raw_response,
                plant_id=plant_id,
                growth_stage=growth_stage,
            )
            
            return analysis
            
        except Exception as e:
            logger.error(f"Model inference failed, using mock: {e}")
            return self._get_mock_analysis(plant_id, growth_stage)
    
    def _build_analysis_prompt(self, growth_stage: str) -> str:
        """Build detailed analysis prompt for the model."""
        return f"""Analyze this plant photo carefully. The plant is in the {growth_stage} stage.

Please identify:
1. Overall health status (score 0-100)
2. Any nutrient deficiencies (N, P, K, Ca, Mg, Fe, etc.)
3. Pest infestations (spider mites, thrips, aphids, etc.)
4. Diseases (powdery mildew, bud rot, etc.)
5. Environmental stress signs (heat, light burn, etc.)

For each issue found, provide:
- Issue type and name
- Severity (low/medium/high/critical)
- Affected area (e.g., "lower leaves", "new growth")
- Immediate solutions
- Prevention tips

Also note any positive observations.

Format your response clearly with sections for issues, recommendations, and follow-up timeline."""
    
    def _parse_model_response(
        self,
        response: str,
        plant_id: Optional[int],
        growth_stage: str,
    ) -> Dict[str, Any]:
        """
        Parse model's free-text response into structured format.
        
        Uses keyword extraction and pattern matching.
        """
        from datetime import datetime
        
        # Extract health score
        health_score = self._extract_health_score(response)
        
        # Extract issues
        issues = self._extract_issues(response)
        
        # Extract recommendations
        recommendations = self._extract_recommendations(response)
        
        # Extract positive observations
        positive_obs = self._extract_positive_observations(response)
        
        # Determine follow-up days based on severity
        follow_up_days = self._determine_followup_days(issues)
        
        return {
            "plant_id": plant_id,
            "growth_stage": growth_stage,
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "overall_health_score": health_score,
            "confidence": 0.85,  # TODO: Extract from model if available
            "issues": issues,
            "positive_observations": positive_obs,
            "recommendations": recommendations,
            "follow_up_days": follow_up_days,
            "needs_confirmation": len(issues) > 2,  # Ask user to confirm if multiple issues
            "raw_response": response,  # Keep for debugging
        }
    
    def _extract_health_score(self, response: str) -> int:
        """Extract health score from response text."""
        import re
        
        # Look for patterns like "health score: 75" or "score of 80"
        patterns = [
            r"health\s+score[:\s]+(\d+)",
            r"score\s+of\s+(\d+)",
            r"overall\s+health[:\s]+(\d+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                score = int(match.group(1))
                return min(100, max(0, score))
        
        # Default: estimate based on issue keywords
        issue_keywords = ["deficiency", "pest", "disease", "stress", "problem", "issue"]
        issue_count = sum(1 for kw in issue_keywords if kw in response.lower())
        
        return max(50, 90 - (issue_count * 15))
    
    def _extract_issues(self, response: str) -> list:
        """Extract health issues from response."""
        issues = []
        
        # Common deficiency patterns
        deficiency_patterns = {
            "nitrogen": ["nitrogen", "n deficiency", "yellowing lower leaves"],
            "phosphorus": ["phosphorus", "p deficiency", "purple stems"],
            "potassium": ["potassium", "k deficiency", "brown edges"],
            "calcium": ["calcium", "ca deficiency", "twisted"],
            "magnesium": ["magnesium", "mg deficiency", "interveinal"],
        }
        
        for nutrient, keywords in deficiency_patterns.items():
            if any(kw in response.lower() for kw in keywords):
                severity = self._determine_severity(response, keywords)
                issues.append({
                    "type": "nutrient_deficiency",
                    "name": f"{nutrient.capitalize()} Deficiency",
                    "description": f"{nutrient.capitalize()} deficiency detected",
                    "severity": severity,
                    "confidence": 0.80,
                    "affected_area": self._extract_affected_area(response),
                    "solutions": [
                        f"Increase {nutrient} in feeding schedule",
                        "Check pH levels (6.0-6.5 optimal)",
                        "Monitor progress in 3-5 days"
                    ],
                    "prevention": [
                        "Maintain consistent feeding schedule",
                        "Regular pH monitoring",
                        "Keep detailed grow journal"
                    ],
                })
        
        return issues
    
    def _extract_recommendations(self, response: str) -> list:
        """Extract actionable recommendations."""
        recommendations = []
        
        # Extract sentences with action words
        action_words = ["increase", "decrease", "add", "remove", "adjust", "check", "monitor", "apply"]
        
        sentences = response.split('.')
        for sentence in sentences:
            if any(word in sentence.lower() for word in action_words):
                clean = sentence.strip()
                if clean and len(clean) > 20:  # Filter out fragments
                    recommendations.append(clean)
        
        return recommendations[:5]  # Top 5 recommendations
    
    def _extract_positive_observations(self, response: str) -> list:
        """Extract positive observations."""
        positive = []
        
        positive_keywords = [
            "healthy", "good", "vigorous", "strong", "no signs of",
            "appear normal", "looking well", "vibrant"
        ]
        
        sentences = response.split('.')
        for sentence in sentences:
            if any(kw in sentence.lower() for kw in positive_keywords):
                clean = sentence.strip()
                if clean and len(clean) > 15:
                    positive.append(clean)
        
        return positive[:4]  # Top 4 positive notes
    
    def _determine_severity(self, response: str, keywords: list) -> str:
        """Determine issue severity from context."""
        context = " ".join([
            sent for sent in response.split('.')
            if any(kw in sent.lower() for kw in keywords)
        ])
        
        if any(word in context.lower() for word in ["critical", "severe", "urgent", "immediate"]):
            return "high"
        elif any(word in context.lower() for word in ["moderate", "significant"]):
            return "medium"
        else:
            return "low"
    
    def _extract_affected_area(self, response: str) -> str:
        """Extract affected plant area."""
        areas = {
            "lower leaves": ["lower leaves", "bottom leaves", "older leaves"],
            "upper leaves": ["upper leaves", "top leaves", "newer leaves"],
            "new growth": ["new growth", "young leaves", "tips"],
            "stems": ["stems", "branches"],
            "overall": ["entire plant", "whole plant", "throughout"],
        }
        
        for area, keywords in areas.items():
            if any(kw in response.lower() for kw in keywords):
                return area
        
        return "unspecified"
    
    def _determine_followup_days(self, issues: list) -> int:
        """Determine follow-up timeline based on issues."""
        if not issues:
            return 7  # Weekly check if healthy
        
        severities = [issue.get("severity", "low") for issue in issues]
        
        if "high" in severities or "critical" in severities:
            return 2  # Check in 2 days for serious issues
        elif "medium" in severities:
            return 4  # Check in 4 days for moderate issues
        else:
            return 5  # Check in 5 days for minor issues
    
    def _get_mock_analysis(self, plant_id: Optional[int], growth_stage: str) -> Dict[str, Any]:
        """Fallback mock analysis if model unavailable."""
        from datetime import datetime
        
        return {
            "plant_id": plant_id,
            "growth_stage": growth_stage,
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "overall_health_score": 78,
            "confidence": 0.50,  # Lower confidence for mock
            "issues": [
                {
                    "type": "nutrient_deficiency",
                    "name": "Early Nitrogen Deficiency",
                    "description": "Lower leaves showing slight yellowing, starting from tips",
                    "severity": "low",
                    "confidence": 0.82,
                    "affected_area": "lower fan leaves",
                    "solutions": [
                        "Increase nitrogen in feeding schedule by 10-15%",
                        "Check pH - nitrogen uptake optimal at 6.0-6.5",
                        "Consider foliar feeding for quick response",
                    ],
                    "prevention": [
                        "Monitor lower leaves weekly",
                        "Maintain consistent feeding schedule",
                        "Keep detailed grow journal",
                    ],
                },
            ],
            "positive_observations": [
                "New growth appears vibrant and healthy",
                "No signs of pest activity detected",
                "Leaf structure and color generally good",
                "Stem strength appears adequate",
            ],
            "recommendations": [
                "Address nitrogen deficiency early to prevent spread",
                "Consider pH test of runoff water",
                "Continue monitoring - recheck in 3-5 days",
            ],
            "follow_up_days": 4,
            "needs_confirmation": False,
            "model_backend": "mock",  # Indicate this is mock data
        }
    
    async def get_treatment_plan(
        self,
        issue_type: str,
        severity: str,
        growth_stage: str,
    ) -> Dict[str, Any]:
        """Get detailed treatment plan for a specific issue"""
        
        # Treatment database
        treatments = {
            "nitrogen_deficiency": {
                "immediate_actions": [
                    "Prepare nitrogen-rich feed (increase N by 15%)",
                    "Check and adjust pH to 6.0-6.5",
                    "Optional: Foliar spray with dilute nitrogen solution",
                ],
                "timeline": [
                    {"day": 0, "action": "Apply nitrogen-rich feeding"},
                    {"day": 2, "action": "Monitor for improvement"},
                    {"day": 4, "action": "Follow-up photo analysis"},
                    {"day": 7, "action": "Assess progress, adjust if needed"},
                ],
                "expected_recovery": "5-10 days for visible improvement",
                "warning_signs": [
                    "Yellowing spreading to upper leaves",
                    "Leaves becoming crispy or falling off",
                    "Stunted new growth",
                ],
                "products": [
                    {"name": "Cal-Mag Plus", "type": "supplement"},
                    {"name": "Fish Emulsion", "type": "organic"},
                ],
            },
        }
        
        treatment = treatments.get(issue_type, {
            "message": f"No specific treatment plan for {issue_type}",
            "general_advice": "Consult growing guides or community forums",
        })
        
        return {
            "issue_type": issue_type,
            "severity": severity,
            "growth_stage": growth_stage,
            "treatment_plan": treatment,
        }
    
    async def compare_health_over_time(
        self,
        photo_analyses: List[Dict],
    ) -> Dict[str, Any]:
        """Compare health progression over multiple photos"""
        
        if len(photo_analyses) < 2:
            return {"error": "Need at least 2 analyses to compare"}
            
        # Sort by timestamp
        sorted_analyses = sorted(
            photo_analyses,
            key=lambda x: x.get("analysis_timestamp", "")
        )
        
        first = sorted_analyses[0]
        last = sorted_analyses[-1]
        
        score_change = (
            last.get("overall_health_score", 0) - 
            first.get("overall_health_score", 0)
        )
        
        return {
            "period": {
                "start": first.get("analysis_timestamp"),
                "end": last.get("analysis_timestamp"),
                "num_analyses": len(photo_analyses),
            },
            "health_trend": {
                "start_score": first.get("overall_health_score"),
                "end_score": last.get("overall_health_score"),
                "change": score_change,
                "trend": "improving" if score_change > 0 else "declining" if score_change < 0 else "stable",
            },
            "resolved_issues": self._find_resolved_issues(first, last),
            "new_issues": self._find_new_issues(first, last),
            "persistent_issues": self._find_persistent_issues(first, last),
        }
    
    def _load_issue_patterns(self) -> Dict[str, Any]:
        """Load issue detection patterns"""
        return {
            "nitrogen_deficiency": {
                "visual_cues": ["yellowing lower leaves", "pale green color"],
                "common_causes": ["underfeeding", "pH lockout", "root issues"],
            },
            "phosphorus_deficiency": {
                "visual_cues": ["purple stems", "dark green leaves", "slow growth"],
                "common_causes": ["cold temperatures", "pH lockout", "underfeeding"],
            },
            "potassium_deficiency": {
                "visual_cues": ["brown leaf edges", "curling leaves", "weak stems"],
                "common_causes": ["underfeeding", "salt buildup", "overwatering"],
            },
            "spider_mites": {
                "visual_cues": ["tiny spots on leaves", "webbing", "yellow stippling"],
                "common_causes": ["dry conditions", "contaminated plants", "poor hygiene"],
            },
            "powdery_mildew": {
                "visual_cues": ["white powder on leaves", "fuzzy patches"],
                "common_causes": ["high humidity", "poor airflow", "temperature swings"],
            },
        }
    
    def _suggest_next_actions(self, analysis: Dict) -> List[str]:
        """Suggest next actions based on analysis"""
        actions = []
        
        if analysis.get("issues"):
            actions.append("view_treatment_plan")
            actions.append("schedule_followup")
            
        if analysis.get("overall_health_score", 100) < 70:
            actions.append("consult_community")
            actions.append("adjust_environment")
            
        actions.append("save_to_journal")
        return actions
    
    def _find_resolved_issues(self, first: Dict, last: Dict) -> List[str]:
        """Find issues that were resolved"""
        first_issues = {i.get("name") for i in first.get("issues", [])}
        last_issues = {i.get("name") for i in last.get("issues", [])}
        return list(first_issues - last_issues)
    
    def _find_new_issues(self, first: Dict, last: Dict) -> List[str]:
        """Find new issues that appeared"""
        first_issues = {i.get("name") for i in first.get("issues", [])}
        last_issues = {i.get("name") for i in last.get("issues", [])}
        return list(last_issues - first_issues)
    
    def _find_persistent_issues(self, first: Dict, last: Dict) -> List[str]:
        """Find issues that persist"""
        first_issues = {i.get("name") for i in first.get("issues", [])}
        last_issues = {i.get("name") for i in last.get("issues", [])}
        return list(first_issues & last_issues)


# Register agent
AgentRegistry.register(PlantHealthVisionAgent())
