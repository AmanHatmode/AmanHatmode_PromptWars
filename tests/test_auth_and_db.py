import pytest
from auth_service import AuthService
from db_service import DatabaseService
from config import Config

def test_auth_service_guest_mode():
    auth = AuthService()
    session = auth.get_guest_session()
    assert session["id"] == "judge-guest-session"
    assert "role" in session
    assert "@" in session["email"]

def test_auth_service_user_formatting():
    auth = AuthService()
    mock_dict = {"id": "123", "email": "user@example.com", "role": "User"}
    formatted = auth._format_user(mock_dict)
    assert formatted["id"] == "123"
    assert formatted["email"] == "user@example.com"

def test_db_service_fallback():
    db = DatabaseService(None)
    save_res = db.save_evaluation("user-1", "My decision text", {"test": "data"})
    assert save_res is True

    history = db.get_history("user-1")
    assert len(history) == 1
    assert history[0]["decision_text"] == "My decision text"


def test_config_validation():
    assert Config.GEMINI_PRIMARY_MODEL != ""
    assert Config.DEFAULT_TEMPERATURE >= 0.0
    assert isinstance(Config.DEMO_MODE, bool)
