import pytest

from src.app.xss_fix import CommentService


class TestXSSFix:

    def setup_method(self):
        self.service = CommentService()

    def test_create_comment_positive(self):
        comment = self.service.create_comment("user123", "This is a normal comment")
        assert comment["username"] == "user123"
        assert comment["comment"] == "This is a normal comment"
        assert comment["original_length"] == 24

    def test_xss_script_tag_negative(self):
        with pytest.raises(ValueError, match="potentially dangerous content"):
            self.service.create_comment("user", "<script>alert('XSS')</script>")

    def test_xss_javascript_protocol_negative(self):
        with pytest.raises(ValueError, match="potentially dangerous content"):
            self.service.create_comment("user", "javascript:alert('XSS')")

    def test_xss_event_handler_negative(self):
        with pytest.raises(ValueError, match="potentially dangerous content"):
            self.service.create_comment("user", "<img onerror='alert(1)'>")

    def test_html_escaping_positive(self):
        comment = self.service.create_comment("user", "<b>bold</b> & <i>italic</i>")
        assert "&lt;b&gt;" in comment["comment"]
        assert "&amp;" in comment["comment"]
        assert "<b>" not in comment["comment"]

    def test_sql_injection_in_comment_negative(self):
        comment = self.service.create_comment("user", "admin' OR '1'='1")
        assert "'" in comment["comment"]
        assert "OR" in comment["comment"]

    def test_empty_comment_negative(self):
        with pytest.raises(ValueError, match="Comment cannot be empty"):
            self.service.create_comment("user", "")

    def test_whitespace_only_comment_negative(self):
        with pytest.raises(ValueError, match="Comment cannot be empty"):
            self.service.create_comment("user", "   ")

    def test_long_comment_negative(self):
        long_comment = "a" * 1001
        with pytest.raises(ValueError, match="exceeds maximum length"):
            self.service.create_comment("user", long_comment)

    def test_invalid_username_type_negative(self):
        with pytest.raises(ValueError, match="Username must be a non-empty string"):
            self.service.create_comment(None, "comment")

    def test_sanitize_special_chars_positive(self):
        text = self.service.sanitize_input('Test "quotes" & <tags>')
        assert "&quot;" in text or "&#x27;" in text
        assert "&lt;" in text
        assert "&gt;" in text
        assert "&amp;" in text
