"""
Insight synthesis engine - generates clinically meaningful insights using LLM integration.
"""

import json
import time
from datetime import datetime, UTC
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod

from core.models.context import AnalysisContext
from core.models.insight import Insight, InsightSynthesisResult, InsightGenerationRequest
from core.insights.prompts import InsightPromptTemplates
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from config.ai import LLMConfig
from core.llm.gemini_client import GeminiClient, LLMClient


class MockLLMClient(LLMClient):
    """
    Mock LLM client for testing and development.
    
    Provides deterministic responses for testing and fallback scenarios.
    """
    
    def __init__(self):
        """Initialize the mock LLM client."""
        pass
    
    def generate(
        self, 
        prompt: str, 
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate mock content for testing.
        
        Args:
            prompt: Input prompt
            **kwargs: Additional arguments
            
        Returns:
            Mock response with text and metadata
        """
        # Extract category from prompt if possible, otherwise use default
        category = "metabolic"  # Default category
        if "cardiovascular" in prompt.lower():
            category = "cardiovascular"
        elif "inflammatory" in prompt.lower():
            category = "inflammatory"
        elif "organ" in prompt.lower():
            category = "organ"
        elif "nutritional" in prompt.lower():
            category = "nutritional"
        elif "hormonal" in prompt.lower():
            category = "hormonal"
        
        # Create deterministic ID based on prompt hash
        import hashlib
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
        
        # Generate deterministic mock responses based on category
        mock_responses = {
            "metabolic": {
                "insights": [
                    {
                        "id": f"metabolic_insight_{prompt_hash}",
                        "category": "metabolic",
                        "summary": "Your metabolic cluster suggests insulin resistance risk, amplified by reported low activity levels.",
                        "evidence": {
                            "biomarkers": ["glucose", "hba1c", "insulin"],
                            "scores": {"glucose": 0.75, "hba1c": 0.68, "insulin": 0.82},
                            "lifestyle_factors": ["exercise", "diet"]
                        },
                        "confidence": 0.85,
                        "severity": "warning",
                        "recommendations": [
                            "Increase physical activity to at least 150 minutes per week",
                            "Consider reducing refined carbohydrate intake",
                            "Monitor blood glucose levels regularly"
                        ],
                        "biomarkers_involved": ["glucose", "hba1c", "insulin"],
                        "lifestyle_factors": ["exercise", "diet"]
                    }
                ]
            },
            "cardiovascular": {
                "insights": [
                    {
                        "id": f"cardiovascular_insight_{prompt_hash}",
                        "category": "cardiovascular",
                        "summary": "Elevated cholesterol patterns indicate increased cardiovascular risk, particularly given your current lifestyle factors.",
                        "evidence": {
                            "biomarkers": ["total_cholesterol", "ldl_cholesterol", "hdl_cholesterol"],
                            "scores": {"total_cholesterol": 0.72, "ldl_cholesterol": 0.78, "hdl_cholesterol": 0.45},
                            "lifestyle_factors": ["diet", "exercise", "smoking"]
                        },
                        "confidence": 0.88,
                        "severity": "warning",
                        "recommendations": [
                            "Focus on heart-healthy diet with reduced saturated fats",
                            "Increase cardiovascular exercise",
                            "Consider discussing statin therapy with your healthcare provider"
                        ],
                        "biomarkers_involved": ["total_cholesterol", "ldl_cholesterol", "hdl_cholesterol"],
                        "lifestyle_factors": ["diet", "exercise"]
                    }
                ]
            },
            "inflammatory": {
                "insights": [
                    {
                        "id": f"inflammatory_insight_{prompt_hash}",
                        "category": "inflammatory",
                        "summary": "Elevated inflammatory markers suggest chronic inflammation, potentially linked to your stress levels and sleep patterns.",
                        "evidence": {
                            "biomarkers": ["crp", "esr"],
                            "scores": {"crp": 0.65, "esr": 0.58},
                            "lifestyle_factors": ["stress", "sleep"]
                        },
                        "confidence": 0.75,
                        "severity": "info",
                        "recommendations": [
                            "Implement stress management techniques",
                            "Improve sleep quality and duration",
                            "Consider anti-inflammatory dietary changes"
                        ],
                        "biomarkers_involved": ["crp", "esr"],
                        "lifestyle_factors": ["stress", "sleep"]
                    }
                ]
            },
            "organ": {
                "insights": [
                    {
                        "id": f"organ_insight_{prompt_hash}",
                        "category": "organ",
                        "summary": "Liver function markers show mild elevation, which may be related to your alcohol consumption and dietary patterns.",
                        "evidence": {
                            "biomarkers": ["alt", "ast", "ggt"],
                            "scores": {"alt": 0.55, "ast": 0.48, "ggt": 0.62},
                            "lifestyle_factors": ["alcohol", "diet"]
                        },
                        "confidence": 0.70,
                        "severity": "info",
                        "recommendations": [
                            "Reduce alcohol consumption",
                            "Focus on liver-supportive foods",
                            "Monitor liver function regularly"
                        ],
                        "biomarkers_involved": ["alt", "ast", "ggt"],
                        "lifestyle_factors": ["alcohol", "diet"]
                    }
                ]
            },
            "nutritional": {
                "insights": [
                    {
                        "id": f"nutritional_insight_{prompt_hash}",
                        "category": "nutritional",
                        "summary": "Vitamin D levels are below optimal range, which may impact your overall health and immune function.",
                        "evidence": {
                            "biomarkers": ["vitamin_d", "b12", "folate"],
                            "scores": {"vitamin_d": 0.35, "b12": 0.68, "folate": 0.72},
                            "lifestyle_factors": ["diet", "sun_exposure"]
                        },
                        "confidence": 0.90,
                        "severity": "warning",
                        "recommendations": [
                            "Consider vitamin D supplementation",
                            "Increase sun exposure safely",
                            "Include vitamin D-rich foods in your diet"
                        ],
                        "biomarkers_involved": ["vitamin_d", "b12", "folate"],
                        "lifestyle_factors": ["diet"]
                    }
                ]
            },
            "hormonal": {
                "insights": [
                    {
                        "id": f"hormonal_insight_{prompt_hash}",
                        "category": "hormonal",
                        "summary": "Stress hormone levels are elevated, potentially contributing to your reported stress and sleep issues.",
                        "evidence": {
                            "biomarkers": ["cortisol", "testosterone", "estradiol"],
                            "scores": {"cortisol": 0.78, "testosterone": 0.45, "estradiol": 0.52},
                            "lifestyle_factors": ["stress", "sleep", "exercise"]
                        },
                        "confidence": 0.80,
                        "severity": "warning",
                        "recommendations": [
                            "Implement stress reduction techniques",
                            "Prioritize quality sleep",
                            "Consider adaptogenic supplements"
                        ],
                        "biomarkers_involved": ["cortisol", "testosterone", "estradiol"],
                        "lifestyle_factors": ["stress", "sleep"]
                    }
                ]
            }
        }
        
        response_data = mock_responses.get(category, {"insights": []})
        
        # Convert to GeminiClient format
        return {
            "text": str(response_data),  # Convert to string for compatibility
            "candidates": [str(response_data)],
            "model": "mock-llm-client"
        }
    
    def generate_insights(
        self, 
        system_prompt: str, 
        user_prompt: str, 
        category: str
    ) -> Dict[str, Any]:
        """
        Generate insights using mock LLM (implements LLMClient interface).
        
        Args:
            system_prompt: System prompt for the LLM
            user_prompt: User prompt with data
            category: Health category
            
        Returns:
            Mock response with insights
        """
        # Combine system and user prompts
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        return self.generate(full_prompt)


class InsightSynthesizer:
    """Main insight synthesis engine."""
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        """
        Initialize the insight synthesizer.
        
        Args:
            llm_client: LLM client for insight generation (defaults to configured provider)
        """
        # Use provided client or create based on LLM_PROVIDER configuration
        if llm_client:
            self.llm_client = llm_client
        else:
            self.llm_client = self._create_llm_client()
        
        self.prompt_templates = InsightPromptTemplates()
        self.llm_config = LLMConfig
    
    def _create_llm_client(self) -> LLMClient:
        """
        Create LLM client based on configuration with robust error handling.
        
        Returns:
            Configured LLM client (GeminiClient or MockLLMClient)
        """
        try:
            # Validate configuration first
            LLMConfig.validate()
            
            # Try to create Gemini client if configured
            if "gemini" in LLMConfig.PROVIDERS and LLMConfig.is_provider_configured("gemini"):
                print("✅ Creating GeminiClient for production LLM integration")
                return GeminiClient()
            else:
                print("⚠️ Gemini not configured, using MockLLMClient for testing")
                return MockLLMClient()
                
        except ValueError as e:
            print(f"❌ Configuration error: {e}, falling back to MockLLMClient")
            return MockLLMClient()
        except Exception as e:
            print(f"❌ Unexpected error creating LLM client: {e}, falling back to MockLLMClient")
            return MockLLMClient()
    
    def synthesize_insights(
        self, 
        context: AnalysisContext,
        biomarker_scores: Dict[str, Any],
        clustering_results: Dict[str, Any],
        lifestyle_profile: Dict[str, Any],
        requested_categories: Optional[List[str]] = None,
        max_insights_per_category: int = 3
    ) -> InsightSynthesisResult:
        """
        Synthesize insights from analysis context and results.
        
        Args:
            context: Analysis context with user and biomarker data
            biomarker_scores: Biomarker scoring results
            clustering_results: Clustering analysis results
            lifestyle_profile: User lifestyle profile
            requested_categories: Specific categories to generate insights for
            max_insights_per_category: Maximum insights per category
            
        Returns:
            InsightSynthesisResult with generated insights
        """
        start_time = time.time()
        
        # Determine categories to process
        categories = requested_categories or self.prompt_templates.get_supported_categories()
        
        all_insights = []
        categories_covered = []
        
        # Generate insights for each category with robust error handling
        for category in categories:
            try:
                print(f"🔄 Generating insights for category: {category}")
                category_insights = self._generate_category_insights(
                    category=category,
                    context=context,
                    biomarker_scores=biomarker_scores,
                    clustering_results=clustering_results,
                    lifestyle_profile=lifestyle_profile,
                    max_insights=max_insights_per_category
                )
                
                if category_insights:
                    all_insights.extend(category_insights)
                    categories_covered.append(category)
                    print(f"✅ Generated {len(category_insights)} insights for {category}")
                else:
                    print(f"⚠️ No insights generated for {category}")
                    
            except Exception as e:
                print(f"❌ Error generating insights for category {category}: {e}")
                # Continue with other categories instead of failing completely
                continue
        
        # Calculate overall confidence
        overall_confidence = self._calculate_overall_confidence(all_insights)
        
        # Calculate LLM usage statistics
        total_tokens_used = sum(insight.tokens_used for insight in all_insights)
        total_latency_ms = sum(insight.latency_ms for insight in all_insights)
        
        # Create synthesis summary
        synthesis_summary = {
            "categories_processed": len(categories),
            "categories_with_insights": len(categories_covered),
            "total_insights_generated": len(all_insights),
            "processing_time_ms": int((time.time() - start_time) * 1000),
            "llm_calls_made": len(categories_covered),
            "total_tokens_used": total_tokens_used,
            "total_latency_ms": total_latency_ms,
            "llm_provider": getattr(self.llm_client, 'model_name', 'unknown')
        }
        
        return InsightSynthesisResult(
            analysis_id=context.analysis_id,
            insights=all_insights,
            synthesis_summary=synthesis_summary,
            total_insights=len(all_insights),
            categories_covered=categories_covered,
            overall_confidence=overall_confidence,
            processing_time_ms=synthesis_summary["processing_time_ms"],
            created_at=datetime.now(UTC).isoformat()
        )
    
    def _generate_category_insights(
        self,
        category: str,
        context: AnalysisContext,
        biomarker_scores: Dict[str, Any],
        clustering_results: Dict[str, Any],
        lifestyle_profile: Dict[str, Any],
        max_insights: int
    ) -> List[Insight]:
        """
        Generate insights for a specific category.
        
        Args:
            category: Health category
            context: Analysis context
            biomarker_scores: Biomarker scoring results
            clustering_results: Clustering analysis results
            lifestyle_profile: User lifestyle profile
            max_insights: Maximum insights to generate
            
        Returns:
            List of Insight objects
        """
        # Format the prompt template
        user_prompt = self.prompt_templates.format_template(
            category=category,
            biomarker_scores=biomarker_scores,
            lifestyle_profile=lifestyle_profile,
            clustering_results=clustering_results
        )
        
        # Get system prompt
        system_prompt = self.prompt_templates.get_system_prompt()
        
        # Generate insights using LLM
        llm_response = self.llm_client.generate_insights(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            category=category
        )
        
        # Parse and validate insights
        insights = self._parse_llm_response(llm_response, category, context.analysis_id)
        
        # Limit to max_insights
        return insights[:max_insights]
    
    def _parse_llm_response(
        self, 
        llm_response: Dict[str, Any], 
        category: str, 
        analysis_id: str
    ) -> List[Insight]:
        """
        Parse LLM response into Insight objects.
        
        Args:
            llm_response: Raw LLM response
            category: Health category
            analysis_id: Analysis identifier
            
        Returns:
            List of parsed Insight objects
        """
        insights = []
        
        try:
            # Check for errors in LLM response
            if "error" in llm_response:
                print(f"⚠️ LLM error for {category}: {llm_response['error']}")
                return []
            
            # Handle new GeminiClient format
            if "text" in llm_response and llm_response["text"]:
                # Try to parse JSON from text response
                import json
                try:
                    response_text = llm_response["text"]
                    if isinstance(response_text, str):
                        # Clean JSON if wrapped in markdown
                        if response_text.startswith("```json"):
                            response_text = response_text[7:]
                        if response_text.endswith("```"):
                            response_text = response_text[:-3]
                        response_text = response_text.strip()
                        
                        parsed_response = json.loads(response_text)
                        raw_insights = parsed_response.get("insights", [])
                    else:
                        raw_insights = []
                except (json.JSONDecodeError, TypeError) as e:
                    print(f"⚠️ JSON parsing error for {category}: {e}")
                    # Fallback: create a single insight from text
                    raw_insights = [{
                        "id": f"{category}_text_insight",
                        "category": category,
                        "summary": llm_response["text"][:200] + "..." if len(llm_response["text"]) > 200 else llm_response["text"],
                        "evidence": {},
                        "confidence": 0.5,
                        "severity": "info",
                        "recommendations": [],
                        "biomarkers_involved": [],
                        "lifestyle_factors": []
                    }]
            else:
                # Fallback to old format
                raw_insights = llm_response.get("insights", [])
            
            for i, raw_insight in enumerate(raw_insights):
                try:
                    # Normalize severity values
                    raw_severity = raw_insight.get("severity", "info")
                    severity_mapping = {
                        "high": "critical",
                        "moderate_risk": "warning", 
                        "low_risk": "info",
                        "protective_factor": "info",
                        "opportunity": "info",
                        "normal": "info",
                        "optimal": "info"
                    }
                    normalized_severity = severity_mapping.get(raw_severity.lower(), "info")
                    
                    # Normalize category values
                    raw_category = raw_insight.get("category", category)
                    category_mapping = {
                        "protective_factor": "metabolic",
                        "cardiovascular_metabolic_crossover": "cardiovascular",
                        "metabolic_syndrome_risk": "metabolic",
                        "inflammatory": "inflammatory",
                        "cardiovascular": "cardiovascular",
                        "metabolic": "metabolic"
                    }
                    normalized_category = category_mapping.get(raw_category.lower(), category)
                    
                    # Create Insight object
                    insight = Insight(
                        id=raw_insight.get("id", f"{category}_insight_{i+1}"),
                        category=normalized_category,
                        summary=raw_insight.get("summary", ""),
                        evidence=raw_insight.get("evidence", {}),
                        confidence=raw_insight.get("confidence", 0.5),
                        severity=normalized_severity,
                        recommendations=raw_insight.get("recommendations", []),
                        biomarkers_involved=raw_insight.get("biomarkers_involved", []),
                        lifestyle_factors=raw_insight.get("lifestyle_factors", []),
                        tokens_used=llm_response.get("tokens_used", 0),
                        latency_ms=llm_response.get("latency_ms", 0),
                        created_at=datetime.now(UTC).isoformat()
                    )
                    
                    insights.append(insight)
                    
                except Exception as e:
                    print(f"Error parsing insight {i}: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error parsing LLM response: {e}")
        
        return insights
    
    def _calculate_overall_confidence(self, insights: List[Insight]) -> float:
        """
        Calculate overall confidence score from individual insights.
        
        Args:
            insights: List of Insight objects
            
        Returns:
            Overall confidence score (0-1)
        """
        if not insights:
            return 0.0
        
        # Calculate weighted average confidence
        total_confidence = sum(insight.confidence for insight in insights)
        return total_confidence / len(insights)
    
    def get_supported_categories(self) -> List[str]:
        """
        Get list of supported health categories.
        
        Returns:
            List of supported categories
        """
        return self.prompt_templates.get_supported_categories()
    
    def validate_insight_request(self, request: InsightGenerationRequest) -> bool:
        """
        Validate an insight generation request.
        
        Args:
            request: Insight generation request
            
        Returns:
            True if request is valid, False otherwise
        """
        try:
            # Check required fields
            if not request.analysis_id:
                return False
            
            if not request.context_data:
                return False
            
            # Check category validity
            supported_categories = self.get_supported_categories()
            for category in request.requested_categories:
                if category not in supported_categories:
                    return False
            
            return True
            
        except Exception:
            return False
