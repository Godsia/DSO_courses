import re
from typing import Optional


class InputValidator:

    @staticmethod
    def validate_username(username: str, min_length: int = 3, max_length: int = 50) -> tuple[bool, Optional[str]]:
        if not username or not isinstance(username, str):
            return False, "Username must be a non-empty string"
        
        if len(username) < min_length:
            return False, f"Username must be at least {min_length} characters long"
        
        if len(username) > max_length:
            return False, f"Username must not exceed {max_length} characters"
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            return False, "Username can only contain letters, numbers, underscores, and hyphens"
        
        return True, None

    @staticmethod
    def validate_email(email: str) -> tuple[bool, Optional[str]]:
        if not email or not isinstance(email, str):
            return False, "Email must be a non-empty string"
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "Invalid email format"
        
        if len(email) > 254:
            return False, "Email address is too long"
        
        return True, None

    @staticmethod
    def validate_string_length(
        text: str, 
        min_length: int = 1, 
        max_length: int = 1000,
        field_name: str = "Field"
    ) -> tuple[bool, Optional[str]]:
        if not isinstance(text, str):
            return False, f"{field_name} must be a string"
        
        if len(text) < min_length:
            return False, f"{field_name} must be at least {min_length} characters long"
        
        if len(text) > max_length:
            return False, f"{field_name} must not exceed {max_length} characters"
        
        return True, None

    @staticmethod
    def sanitize_for_logging(text: str) -> str:
        if not isinstance(text, str):
            return str(text)
        
        sanitized = re.sub(r'[\n\r\t]', ' ', text)
        sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', sanitized)
        
        return sanitized[:500]
