from typing import Optional, Dict, Any
from config import Config

class AuthService:
    def __init__(self):
        self.supabase_client = None
        self._initialize_supabase()

    def _initialize_supabase(self):
        if Config.is_supabase_configured():
            try:
                from supabase import create_client
                self.supabase_client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
            except Exception as e:
                print(f"[AuthService] Supabase initialization failed: {e}")
                self.supabase_client = None

    @property
    def is_cloud_enabled(self) -> bool:
        return self.supabase_client is not None

    def _format_user(self, user) -> Dict[str, Any]:
        """Convert Supabase User object or dict into a standard dictionary"""
        if isinstance(user, dict):
            return user
        return {
            "id": getattr(user, "id", "user"),
            "email": getattr(user, "email", "Verified User"),
            "role": getattr(user, "role", "Authenticated User")
        }

    def sign_up(self, email: str, password: str) -> Dict[str, Any]:
        """Sign up a new user via Supabase Auth"""
        if not self.is_cloud_enabled:
            # Fallback for local demo mode
            return {
                "success": True, 
                "user": {"id": "demo-user-123", "email": email, "role": "Standard User"}, 
                "message": "Demo mode: Account registered successfully (Local session)."
            }

        try:
            res = self.supabase_client.auth.sign_up({"email": email, "password": password})
            if res.user:
                return {"success": True, "user": self._format_user(res.user), "message": "Sign up successful! Please check your email if confirmation is enabled."}
            return {"success": False, "message": "Could not create user account."}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        """Sign in an existing user with email and password"""
        if not self.is_cloud_enabled:
            # Fallback for local demo mode
            return {
                "success": True, 
                "user": {"id": "demo-user-123", "email": email, "role": "Standard User"}, 
                "message": "Demo mode: Signed in successfully as Guest/Demo Judge."
            }

        try:
            res = self.supabase_client.auth.sign_in_with_password({"email": email, "password": password})
            if res.user:
                return {"success": True, "user": self._format_user(res.user), "message": "Login successful!"}
            return {"success": False, "message": "Invalid email or password."}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def sign_out(self) -> Dict[str, Any]:
        """Sign out the active user"""
        if not self.is_cloud_enabled:
            return {"success": True, "message": "Signed out of local demo session."}

        try:
            self.supabase_client.auth.sign_out()
            return {"success": True, "message": "Signed out successfully."}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def get_guest_session(self) -> Dict[str, Any]:
        """Instant access for hackathon judges evaluating the tool without signup friction"""
        return {
            "id": "judge-guest-session",
            "email": "judge.evaluator@promptwars.ai",
            "role": "Hackathon Judge (Guest Access)"
        }
