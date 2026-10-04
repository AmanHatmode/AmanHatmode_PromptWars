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

    # Validate Cognitive Legitimacy & Scientific Framework fields
    assert analysis.epistemic_rigor is not None
    assert 0 <= analysis.epistemic_rigor.bias_density_score <= 100
    assert 0 <= analysis.epistemic_rigor.assumption_fragility_index <= 100
    assert analysis.epistemic_rigor.decision_framework_applied != ""
    assert all(a.falsification_protocol != "" for a in analysis.unstated_assumptions)
    assert all(r.stress_test_question != "" for r in analysis.overlooked_risks)
    assert all(b.framework_reference != "" for b in analysis.cognitive_biases)

def test_startup_scenario_schema(engine):
    """Test that startup scenario evaluates with proper risk categorization and epistemic rigor"""
    scenario = "I want to drop out of college to launch my AI prototype full-time because my friends love it."
    result = engine.evaluate_decision(scenario)
    assert result["success"] is True
    analysis = BlindSpotAnalysis(**result["data"])
    assert any(r.risk_category == "Financial" for r in analysis.overlooked_risks)
    assert analysis.epistemic_rigor.risk_exposure_level == "High Systemic Risk"

def test_architecture_scenario_schema(engine):
    """Test technical architecture pivot scenario"""
    scenario = "We are planning to split our monolithic Python application into microservices running on Kubernetes."
    result = engine.evaluate_decision(scenario)
    assert result["success"] is True
    analysis = BlindSpotAnalysis(**result["data"])
    assert any("Premature Optimization" in b.name for b in analysis.cognitive_biases)

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

def test_followup_evaluation(engine):
    """Test Socratic defense evaluation"""
    res = engine.evaluate_followup(
        decision_context="Accepting 35k internship",
        question_asked="What if the dean rejects medical notes?",
        user_answer="I will talk to my professor to informally manage my attendance."
    )
    assert res["success"] is True
    assert "reflection" in res

