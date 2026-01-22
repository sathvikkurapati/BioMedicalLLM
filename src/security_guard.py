import re

class SecurityGuard:
    def __init__(self):
        self.unsafe_keywords = [
            "kill", "suicide", "bomb", "poison", "murder", 
            "hack", "bypass", "ignore instructions"
        ]
        # Regex for common PII (Email, Phone - generic)
        self.pii_patterns = {
            "EMAIL": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "PHONE": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        }
        
    def check_input(self, text):
        """
        Validates input prompt.
        Returns: (is_safe: bool, reason: str)
        """
        text_lower = text.lower()
        
        # Check for jailbreak patterns
        if "ignore previous instructions" in text_lower or "system prompt" in text_lower:
            return False, "Potential jailbreak attempt detected. Request blocked."
            
        # Check for harmful keywords
        for kw in self.unsafe_keywords:
            if kw in text_lower:
                return False, f"Unsafe content detected: '{kw}'. Request blocked."
                
        return True, "Safe"

    def sanitize_output(self, text):
        """
        Sanitizes model output to remove PII.
        """
        sanitized_text = text
        for pii_type, pattern in self.pii_patterns.items():
            sanitized_text = re.sub(pattern, f"[{pii_type} REDACTED]", sanitized_text)
            
        return sanitized_text
