import logging
import re
from typing import Any


class SecureLogger:

    EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    PHONE_PATTERN = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
    SSN_PATTERN = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
    CREDIT_CARD_PATTERN = re.compile(r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b')

    def __init__(self, name: str = "secure_app", level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(level)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def _mask_pii(self, message: str) -> str:
        message = self.EMAIL_PATTERN.sub('[EMAIL_REDACTED]', message)
        
        message = self.PHONE_PATTERN.sub('[PHONE_REDACTED]', message)
        
        message = self.SSN_PATTERN.sub('[SSN_REDACTED]', message)
        
        message = self.CREDIT_CARD_PATTERN.sub('[CARD_REDACTED]', message)
        
        return message

    def info(self, message: str, *args: Any, **kwargs: Any):
        safe_message = self._mask_pii(str(message))
        self.logger.info(safe_message, *args, **kwargs)

    def warning(self, message: str, *args: Any, **kwargs: Any):
        safe_message = self._mask_pii(str(message))
        self.logger.warning(safe_message, *args, **kwargs)

    def error(self, message: str, *args: Any, **kwargs: Any):
        safe_message = self._mask_pii(str(message))
        self.logger.error(safe_message, *args, **kwargs)

    def debug(self, message: str, *args: Any, **kwargs: Any):
        safe_message = self._mask_pii(str(message))
        self.logger.debug(safe_message, *args, **kwargs)
