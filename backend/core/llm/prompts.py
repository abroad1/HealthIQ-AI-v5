"""
Prompt templates for Gemini LLM integration.

This module defines structured prompt templates for biomarker analysis,
insight synthesis, and narrative generation using Google Gemini.
"""

from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class PromptType(Enum):
    """Types of prompts available."""
    BIOMARKER_PARSING = "biomarker_parsing"
    INSIGHT_SYNTHESIS = "insight_synthesis"
    NARRATIVE_GENERATION = "narrative_generation"
    RECOMMENDATION_GENERATION = "recommendation_generation"


@dataclass
class PromptTemplate:
    """Template for a specific prompt type."""
    name: str
    template: str
    variables: List[str]
    output_schema: Dict[str, Any]


class PromptTemplates:
    """Collection of prompt templates for HealthIQ AI v5."""
    
    @staticmethod
    def get_biomarker_parsing_prompt() -> PromptTemplate:
        """Get prompt template for biomarker parsing."""
        return PromptTemplate(
            name="biomarker_parsing",
            template="""You are a medical data extraction specialist. Extract biomarker values from the following text and return them in a structured format.

Text to analyze:
{text_content}

Instructions:
1. Identify all biomarker values mentioned in the text
2. Extract the numerical value and unit for each biomarker
3. Use canonical biomarker names from the provided list
4. If a biomarker is mentioned but no value is given, mark it as missing
5. Return only valid biomarker data

Canonical biomarker names:
{canonical_biomarkers}

Return your response as a JSON object with this structure:
{{
    "biomarkers": {{
        "biomarker_name": {{
            "value": number,
            "unit": "string",
            "confidence": number (0-1)
        }}
    }},
    "extraction_notes": "string",
    "confidence_score": number (0-1)
}}""",
            variables=["text_content", "canonical_biomarkers"],
            output_schema={
                "type": "object",
                "properties": {
                    "biomarkers": {
                        "type": "object",
                        "additionalProperties": {
                            "type": "object",
                            "properties": {
                                "value": {"type": "number"},
                                "unit": {"type": "string"},
                                "confidence": {"type": "number", "minimum": 0, "maximum": 1}
                            },
                            "required": ["value", "unit", "confidence"]
                        }
                    },
                    "extraction_notes": {"type": "string"},
                    "confidence_score": {"type": "number", "minimum": 0, "maximum": 1}
                },
                "required": ["biomarkers", "extraction_notes", "confidence_score"]
            }
        )
    
    @staticmethod
    def get_insight_synthesis_prompt() -> PromptTemplate:
        """Get prompt template for insight synthesis."""
        return PromptTemplate(
            name="insight_synthesis",
            template="""You are a clinical biomarker analysis expert. Analyze the provided biomarker data and generate clinically relevant insights.

Biomarker Data:
{biomarker_data}

Scoring Results:
{scoring_results}

Clustering Results:
{clustering_results}

User Profile:
{user_profile}

Instructions:
1. Analyze the biomarker patterns and identify key health insights
2. Consider the scoring results and clustering patterns
3. Generate actionable insights based on clinical best practices
4. Focus on metabolic, cardiovascular, inflammatory, and organ health
5. Provide evidence-based recommendations
6. Use clear, patient-friendly language

Return your response as a JSON object with this structure:
{{
    "insights": [
        {{
            "category": "string",
            "title": "string",
            "description": "string",
            "severity": "low|moderate|high|critical",
            "confidence": number (0-1),
            "evidence": ["string"],
            "recommendations": ["string"]
        }}
    ],
    "overall_assessment": "string",
    "key_findings": ["string"],
    "next_steps": ["string"]
}}""",
            variables=["biomarker_data", "scoring_results", "clustering_results", "user_profile"],
            output_schema={
                "type": "object",
                "properties": {
                    "insights": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "category": {"type": "string"},
                                "title": {"type": "string"},
                                "description": {"type": "string"},
                                "severity": {"type": "string", "enum": ["low", "moderate", "high", "critical"]},
                                "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                                "evidence": {"type": "array", "items": {"type": "string"}},
                                "recommendations": {"type": "array", "items": {"type": "string"}}
                            },
                            "required": ["category", "title", "description", "severity", "confidence", "evidence", "recommendations"]
                        }
                    },
                    "overall_assessment": {"type": "string"},
                    "key_findings": {"type": "array", "items": {"type": "string"}},
                    "next_steps": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["insights", "overall_assessment", "key_findings", "next_steps"]
            }
        )
    
    @staticmethod
    def get_narrative_generation_prompt() -> PromptTemplate:
        """Get prompt template for narrative generation."""
        return PromptTemplate(
            name="narrative_generation",
            template="""You are a medical writer creating patient-friendly health reports. Generate a clear, actionable narrative based on the biomarker analysis.

Analysis Results:
{analysis_results}

User Profile:
{user_profile}

Instructions:
1. Create a patient-friendly narrative explaining the health findings
2. Use clear, non-technical language
3. Focus on actionable insights and recommendations
4. Maintain a supportive, encouraging tone
5. Highlight both positive findings and areas for improvement
6. Provide specific, evidence-based recommendations

Return your response as a JSON object with this structure:
{{
    "executive_summary": "string",
    "detailed_analysis": "string",
    "key_recommendations": ["string"],
    "positive_findings": ["string"],
    "areas_for_improvement": ["string"],
    "next_steps": ["string"]
}}""",
            variables=["analysis_results", "user_profile"],
            output_schema={
                "type": "object",
                "properties": {
                    "executive_summary": {"type": "string"},
                    "detailed_analysis": {"type": "string"},
                    "key_recommendations": {"type": "array", "items": {"type": "string"}},
                    "positive_findings": {"type": "array", "items": {"type": "string"}},
                    "areas_for_improvement": {"type": "array", "items": {"type": "string"}},
                    "next_steps": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["executive_summary", "detailed_analysis", "key_recommendations", "positive_findings", "areas_for_improvement", "next_steps"]
            }
        )
    
    @staticmethod
    def get_recommendation_generation_prompt() -> PromptTemplate:
        """Get prompt template for recommendation generation."""
        return PromptTemplate(
            name="recommendation_generation",
            template="""You are a clinical nutritionist and lifestyle medicine expert. Generate personalized recommendations based on biomarker analysis.

Biomarker Analysis:
{biomarker_analysis}

User Profile:
{user_profile}

Lifestyle Factors:
{lifestyle_factors}

Instructions:
1. Generate personalized, evidence-based recommendations
2. Focus on nutrition, exercise, sleep, stress management, and supplements
3. Consider the user's current lifestyle and preferences
4. Provide specific, actionable steps
5. Include both short-term and long-term recommendations
6. Prioritize recommendations by impact and feasibility

Return your response as a JSON object with this structure:
{{
    "nutrition_recommendations": ["string"],
    "exercise_recommendations": ["string"],
    "lifestyle_recommendations": ["string"],
    "supplement_recommendations": ["string"],
    "monitoring_recommendations": ["string"],
    "priority_actions": ["string"],
    "timeline": {{
        "immediate": ["string"],
        "short_term": ["string"],
        "long_term": ["string"]
    }}
}}""",
            variables=["biomarker_analysis", "user_profile", "lifestyle_factors"],
            output_schema={
                "type": "object",
                "properties": {
                    "nutrition_recommendations": {"type": "array", "items": {"type": "string"}},
                    "exercise_recommendations": {"type": "array", "items": {"type": "string"}},
                    "lifestyle_recommendations": {"type": "array", "items": {"type": "string"}},
                    "supplement_recommendations": {"type": "array", "items": {"type": "string"}},
                    "monitoring_recommendations": {"type": "array", "items": {"type": "string"}},
                    "priority_actions": {"type": "array", "items": {"type": "string"}},
                    "timeline": {
                        "type": "object",
                        "properties": {
                            "immediate": {"type": "array", "items": {"type": "string"}},
                            "short_term": {"type": "array", "items": {"type": "string"}},
                            "long_term": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["immediate", "short_term", "long_term"]
                    }
                },
                "required": ["nutrition_recommendations", "exercise_recommendations", "lifestyle_recommendations", "supplement_recommendations", "monitoring_recommendations", "priority_actions", "timeline"]
            }
        )
    
    @classmethod
    def get_template(cls, prompt_type: PromptType) -> PromptTemplate:
        """
        Get a prompt template by type.
        
        Args:
            prompt_type: Type of prompt to retrieve
            
        Returns:
            PromptTemplate object
        """
        if prompt_type == PromptType.BIOMARKER_PARSING:
            return cls.get_biomarker_parsing_prompt()
        elif prompt_type == PromptType.INSIGHT_SYNTHESIS:
            return cls.get_insight_synthesis_prompt()
        elif prompt_type == PromptType.NARRATIVE_GENERATION:
            return cls.get_narrative_generation_prompt()
        elif prompt_type == PromptType.RECOMMENDATION_GENERATION:
            return cls.get_recommendation_generation_prompt()
        else:
            raise ValueError(f"Unknown prompt type: {prompt_type}")
    
    @classmethod
    def format_prompt(cls, prompt_type: PromptType, **kwargs) -> str:
        """
        Format a prompt template with variables.
        
        Args:
            prompt_type: Type of prompt to format
            **kwargs: Variables to substitute in the template
            
        Returns:
            Formatted prompt string
        """
        template = cls.get_template(prompt_type)
        return template.template.format(**kwargs)
