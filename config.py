import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

class Config:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    # Models
    GEMINI_PRIMARY_MODEL: str = "gemini-3.8-flash"
    GEMINI_FAST_MODEL: str = "gemini-3.8-flash"
    
    # Execution thresholds
    DEFAULT_TEMPERATURE: float = 0.3  # Analytical rigor, low hallucination
    MAX_TOKENS: int = 2048
    
    # Flag to allow offline demo fallback if API keys are not supplied during live judging
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "True").lower() in ("true", "1", "yes")

    @classmethod
    def is_gemini_configured(cls) -> bool:
        return bool(cls.GEMINI_API_KEY and not cls.GEMINI_API_KEY.startswith("your_"))

    @classmethod
    def is_supabase_configured(cls) -> bool:
        return bool(
            cls.SUPABASE_URL 
            and cls.SUPABASE_KEY 
            and not cls.SUPABASE_URL.startswith("https://your-project-id")
        )
