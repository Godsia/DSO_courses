import html
import re
from typing import Optional


class CommentService:

    @staticmethod
    def sanitize_input(text: str) -> str:
        if not isinstance(text, str):
            raise ValueError("Input must be a string")
        
        sanitized = html.escape(text, quote=True)
        
        return sanitized

    @staticmethod
    def validate_comment(comment: str, max_length: int = 1000) -> tuple[bool, Optional[str]]:
        if not comment or not isinstance(comment, str):
            return False, "Comment must be a non-empty string"
        
        if len(comment.strip()) == 0:
            return False, "Comment cannot be empty"
        
        if len(comment) > max_length:
            return False, f"Comment exceeds maximum length of {max_length} characters"
        
        dangerous_patterns = [
            r'<script[^>]*>',
            r'javascript:',
            r'on\w+\s*=',
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, comment, re.IGNORECASE):
                return False, "Comment contains potentially dangerous content"
        
        return True, None

    def create_comment(self, username: str, comment: str) -> dict:
        if not username or not isinstance(username, str):
            raise ValueError("Username must be a non-empty string")
        
        is_valid, error_msg = self.validate_comment(comment)
        if not is_valid:
            raise ValueError(error_msg or "Invalid comment")
        
        safe_username = self.sanitize_input(username)
        safe_comment = self.sanitize_input(comment)
        
        return {
            "username": safe_username,
            "comment": safe_comment,
            "original_length": len(comment)
        }
