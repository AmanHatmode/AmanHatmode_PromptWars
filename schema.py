from pydantic import BaseModel, Field
from typing import List, Literal, Dict

class CognitiveBias(BaseModel):
    name: str = Field(..., description="Name of cognitive bias")
    description: str = Field(..., description="How this bias distorts the user's reasoning")
    severity: Literal["Low", "Medium", "High"] = Field(..., description="Distortion severity")

class Assumption(BaseModel):
    premise: str = Field(..., description="Unstated premise or hypothesis taken for granted")
    category: Literal["Feasibility & Bandwidth", "Quality & Value", "Policy & Institutional", "Financial & Career"] = Field(
        ..., description="Domain category of the assumption"
    )
    confidence_level: Literal["Unverified Guess", "Fragile Anecdote", "Partial Fact"] = Field(
        default="Unverified Guess", description="Reliability level of this premise"
    )
    vulnerability: str = Field(..., description="Why this assumption is fragile")

class OverlookedRisk(BaseModel):
    risk_title: str = Field(..., description="Concise title of the risk")
    risk_category: Literal["Financial", "Operational", "Personal & Academic"] = Field(
        default="Operational", description="Broad category of risk"
    )
    risk_type: Literal["Immediate Operational", "Long-Term Opportunity Cost", "Second-Order Consequence"] = Field(
        ..., description="Temporal/systemic nature"
    )
    failure_scenario: str = Field(..., description="How this risk materializes")
    severity: Literal["Moderate", "High", "Critical"] = Field(..., description="Impact severity")

class AlternativePerspective(BaseModel):
    stakeholder: str = Field(..., description="Role/Persona (e.g. University Dean, Senior Staff Engineer, Tier-1 Recruiter)")
    contrarian_view: str = Field(..., description="What this stakeholder notices that the user ignores")
    key_question_they_would_ask: str = Field(..., description="The sharp question this stakeholder would ask")

class PreMortemTimeline(BaseModel):
    one_month: str = Field(..., description="Initial friction appearing at 1 month")
    six_months: str = Field(..., description="Compounding failure state at 6 months")
    one_year: str = Field(..., description="Long-term regret or structural consequence at 1 year")

class SocraticQuestion(BaseModel):
    domain: str = Field(..., description="Area of inquiry")
    question: str = Field(..., description="Probing open-ended question")
    reflection_prompt: str = Field(..., description="Investigation guidance")

class BlindSpotAnalysis(BaseModel):
    decision_summary: str = Field(..., description="Objective summary of the decision")
    thoughtfulness_score: int = Field(
        ..., ge=0, le=100, 
        description="Reasoning completeness score from 0-100 (NOT offer quality)"
    )
    salient_factors: List[str] = Field(
        ..., description="Immediate visible perks the user is fixated on"
    )
    cognitive_biases: List[CognitiveBias] = Field(..., description="Identified cognitive biases")
    unstated_assumptions: List[Assumption] = Field(..., description="Unstated assumptions with confidence levels")
    overlooked_risks: List[OverlookedRisk] = Field(..., description="Risks categorized into Financial, Operational, Personal")
    alternative_perspectives: List[AlternativePerspective] = Field(
        default_factory=list, description="Viewpoints from critical external stakeholders"
    )
    pre_mortem_timeline: PreMortemTimeline = Field(
        ..., description="Time-stepped pre-mortem simulation (1 month, 6 months, 1 year)"
    )
    socratic_questions: List[SocraticQuestion] = Field(
        ..., description="3 targeted Socratic questions"
    )
    non_prescriptive_guarantee: str = Field(
        default="The Blind Spot never decides for you. It illuminates what you cannot see so you can decide with 100% clarity.",
        description="Constitutional guarantee preserving 100% human agency"
    )
