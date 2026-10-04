from typing import List, Dict, Any
from config import Config
import json
import datetime

class DatabaseService:
    def __init__(self, supabase_client=None):
        self.supabase = supabase_client
        self._local_history: List[Dict[str, Any]] = []

    def save_evaluation(self, user_id: str, decision_text: str, evaluation_data: Dict[str, Any]) -> bool:
        """
        Saves decision analysis to Supabase Postgres.
        Falls back to local session store if Supabase DB is offline or in demo mode.
        """
        record = {
            "user_id": user_id,
            "decision_text": decision_text,
            "analysis": evaluation_data,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # In-memory storage for instant UI retrieval
        self._local_history.insert(0, record)

        if self.supabase:
            try:
                # Target Supabase table 'decision_evaluations'
                self.supabase.table("decision_evaluations").insert({
                    "user_id": user_id,
                    "decision_text": decision_text,
                    "analysis_json": json.dumps(evaluation_data),
                    "created_at": record["created_at"]
                }).execute()
                return True
            except Exception as e:
                print(f"[DatabaseService] Cloud DB save failed, cached locally: {e}")
                return False
        return True

    def get_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Retrieves history for the current user"""
        if self.supabase:
            try:
                response = self.supabase.table("decision_evaluations")\
                    .select("*")\
                    .eq("user_id", user_id)\
                    .order("created_at", desc=True)\
                    .limit(10)\
                    .execute()
                if response.data:
                    return [
                        {
                            "user_id": row.get("user_id"),
                            "decision_text": row.get("decision_text"),
                            "analysis": json.loads(row.get("analysis_json", "{}")),
                            "created_at": row.get("created_at")
                        }
                        for row in response.data
                    ]
            except Exception as e:
                print(f"[DatabaseService] Cloud DB fetch error: {e}")

        # Fallback to local session history
        return [item for item in self._local_history if item["user_id"] == user_id]
