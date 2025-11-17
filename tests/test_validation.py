
from src.app.validation import InputValidator


class TestInputValidator:

    def setup_method(self):
        self.validator = InputValidator()

    def test_validate_username_positive(self):
        is_valid, error = self.validator.validate_username("testuser123")
        assert is_valid is True
        assert error is None

    def test_validate_username_too_short_negative(self):
        is_valid, error = self.validator.validate_username("ab")
        assert is_valid is False
        assert "at least" in error.lower()

    def test_validate_username_too_long_negative(self):
        long_username = "a" * 51
        is_valid, error = self.validator.validate_username(long_username)
        assert is_valid is False
        assert "exceed" in error.lower()

    def test_validate_username_invalid_chars_negative(self):
        is_valid, error = self.validator.validate_username("user@name")
        assert is_valid is False
        assert "only contain" in error.lower()

    def test_validate_username_empty_negative(self):
        is_valid, error = self.validator.validate_username("")
        assert is_valid is False

    def test_validate_email_positive(self):
        is_valid, error = self.validator.validate_email("test@example.com")
        assert is_valid is True
        assert error is None

    def test_validate_email_invalid_format_negative(self):
        is_valid, error = self.validator.validate_email("notanemail")
        assert is_valid is False
        assert "format" in error.lower()

    def test_validate_email_no_at_negative(self):
        is_valid, error = self.validator.validate_email("testexample.com")
        assert is_valid is False

    def test_validate_email_empty_negative(self):
        is_valid, error = self.validator.validate_email("")
        assert is_valid is False

    def test_validate_string_length_positive(self):
        is_valid, error = self.validator.validate_string_length("test", 1, 10)
        assert is_valid is True
        assert error is None

    def test_validate_string_length_too_short_negative(self):
        is_valid, error = self.validator.validate_string_length("", 1, 10)
        assert is_valid is False

    def test_validate_string_length_too_long_negative(self):
        long_string = "a" * 101
        is_valid, error = self.validator.validate_string_length(long_string, 1, 100)
        assert is_valid is False

    def test_sanitize_for_logging_positive(self):
        text = "test\nwith\ttabs"
        sanitized = self.validator.sanitize_for_logging(text)
        assert "\n" not in sanitized
        assert "\t" not in sanitized
