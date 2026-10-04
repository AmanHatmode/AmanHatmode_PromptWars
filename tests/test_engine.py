import pytest
from engine import BlindSpotEngine
from schema import BlindSpotAnalysis
from guardrails import SecurityGuardrails

@pytest.fixture
def engine():
    return BlindSpotEngine()

def test_internship_scenario_schema(engine):
    """Test that the engine evaluates the challenge internship scenario and returns valid upgraded schema"""
    scenario = (
        "I am deciding whether to accept a 6-month internship at a consultancy. "
        "The stipend is 35k and it is 15 minutes away, but my college has 75% attendance rules."
    )
    result = engine.evaluate_decision(scenario)
    assert result["success"] is True
    assert result["data"] is not None

    # Validate against Pydantic schema
    analysis = BlindSpotAnalysis(**result["data"])
    assert 0 <= analysis.thoughtfulness_score <= 100
    assert len(analysis.cognitive_biases) >= 1
    assert len(analysis.unstated_assumptions) >= 1
    assert len(analysis.overlooked_risks) >= 1
    assert len(analysis.alternative_perspectives) >= 1
    assert analysis.pre_mortem_timeline.one_month is not None
    assert analysis.pre_mortem_timeline.six_months is not None
    assert analysis.pre_mortem_timeline.one_year is not None
    assert len(analysis.socratic_questions) >= 1

def test_startup_scenario_schema(engine):
    """Test that startup scenario evaluates with proper risk categorization"""
    scenario = "I want to drop out of college to launch my AI prototype full-time because my friends love it."
    result = engine.evaluate_decision(scenario)
    assert result["success"] is True
    analysis = BlindSpotAnalysis(**result["data"])
    assert any(r.risk_category == "Financial" for r in analysis.overlooked_risks)

def test_strict_non_prescriptive_guarantee(engine):
    """Assert that the engine NEVER outputs prescriptive commands (you should accept, reject, etc.)"""
    scenario = "Should I take this internship or stay in college? Tell me what to choose."
    result = engine.evaluate_decision(scenario)
    
    if result["success"] and result["data"]:
        analysis = result["data"]
        full_text = str(analysis)
        is_compliant, violations = SecurityGuardrails.verify_output_compliance(full_text)
        assert is_compliant, f"Violations found: {violations}"
        assert "non_prescriptive_guarantee" in analysis
