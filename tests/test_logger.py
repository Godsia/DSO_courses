import logging
from io import StringIO

from src.app.logger import SecureLogger


class TestSecureLogger:

    def setup_method(self):
        self.logger = SecureLogger("test_logger", level=logging.DEBUG)
        self.stream = StringIO()
        handler = logging.StreamHandler(self.stream)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.logger.addHandler(handler)

    def test_email_masking_positive(self):
        self.logger.info("User email is test@example.com")
        log_output = self.stream.getvalue()
        assert "[EMAIL_REDACTED]" in log_output
        assert "test@example.com" not in log_output

    def test_phone_masking_positive(self):
        self.logger.info("Contact phone: 555-123-4567")
        log_output = self.stream.getvalue()
        assert "[PHONE_REDACTED]" in log_output
        assert "555-123-4567" not in log_output

    def test_ssn_masking_positive(self):
        self.logger.info("SSN: 123-45-6789")
        log_output = self.stream.getvalue()
        assert "[SSN_REDACTED]" in log_output
        assert "123-45-6789" not in log_output

    def test_credit_card_masking_positive(self):
        self.logger.info("Card: 1234-5678-9012-3456")
        log_output = self.stream.getvalue()
        assert "[CARD_REDACTED]" in log_output
        assert "1234-5678-9012-3456" not in log_output

    def test_multiple_pii_masking_positive(self):
        self.logger.info("User test@example.com with phone 555-123-4567")
        log_output = self.stream.getvalue()
        assert "[EMAIL_REDACTED]" in log_output
        assert "[PHONE_REDACTED]" in log_output
        assert "test@example.com" not in log_output
        assert "555-123-4567" not in log_output

    def test_no_pii_logging_positive(self):
        self.logger.info("User logged in successfully")
        log_output = self.stream.getvalue()
        assert "User logged in successfully" in log_output

    def test_error_logging_positive(self):
        self.logger.error("An error occurred")
        log_output = self.stream.getvalue()
        assert "ERROR" in log_output
        assert "An error occurred" in log_output

    def test_warning_logging_positive(self):
        self.logger.warning("Warning: invalid input")
        log_output = self.stream.getvalue()
        assert "WARNING" in log_output
        assert "invalid input" in log_output
