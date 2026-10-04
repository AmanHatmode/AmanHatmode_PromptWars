import re
from typing import Tuple, List

class SecurityGuardrails:
    # Common prompt injection signatures
    INJECTION_PATTERNS: List[str] = [
        r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
        r"system\s+prompt",
        r"you\s+are\s+now\s+(an?\s+)?DAN",
        r"bypass\s+rules",
        r"tell\s+me\s+what\s+(decision\s+to\s+make|to\s+choose)",
        r"choose\s+for\s+me",
        r"make\s+the\s+decision\s+for\s+me",
        r"say\s+yes\s+or\s+no",
        r"just\s+tell\s+me\s+if\s+I\s+should",
        r"disregard\s+guardrails",
    ]

    # Prohibited prescriptive output patterns to preserve 100% human agency
    PRESCRIPTIVE_PATTERNS: List[str] = [
        r"\b(you\s+should\s+(accept|reject|take|decline|quit|stay))\b",
        r"\b(i\s+recommend\s+that\s+you\s+(take|reject|accept))\b",
        r"\b(my\s+advice\s+is\s+to\s+(accept|reject|take))\b",
        r"\b(the\s+best\s+decision\s+is\s+to)\b",
        r"\b(you\s+must\s+(accept|reject|take))\b",
    ]

    @classmethod
    def sanitize_input(cls, user_text: str) -> Tuple[bool, str, str]:
        """
        Validates user input against injection attempts and length limits.
        Returns: (is_safe: bool, sanitized_text: str, reason: str)
        """
        if not user_text or not user_text.strip():
            return False, "", "Input cannot be empty. Please provide context about your decision."

        cleaned = user_text.strip()
        
        if len(cleaned) < 20:
            return False, cleaned, "Input is too brief. Please provide details (e.g., pros, cons, constraints) so blind spots can be evaluated."

        if len(cleaned) > 4000:
            return False, cleaned[:4000], "Input exceeds maximum limit of 4000 characters."

        # Scan for injection patterns
        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, cleaned, re.IGNORECASE):
                return False, cleaned, f"Security violation detected: Input contains adversarial override attempts ('{pattern}')."

        return True, cleaned, "Input passed security validation."

    @classmethod
    def verify_output_compliance(cls, output_text: str) -> Tuple[bool, List[str]]:
        """
        Verifies that the generated analysis does NOT contain prescriptive choices.
        Returns: (is_compliant: bool, violations: List[str])
        """
        violations = []
        for pattern in cls.PRESCRIPTIVE_PATTERNS:
            matches = re.findall(pattern, output_text, re.IGNORECASE)
            if matches:
                violations.append(f"Prescriptive language detected: {matches}")

        return (len(violations) == 0), violations
