import pytest

from src.app.sql_injection_fix import UserService


class TestSQLInjectionFix:

    def setup_method(self):
        self.service = UserService()

    def teardown_method(self):
        self.service.close()

    def test_create_and_get_user_positive(self):
        user = self.service.create_user("testuser", "test@example.com")
        assert user["username"] == "testuser"
        assert user["email"] == "test@example.com"
        
        retrieved = self.service.get_user_by_username("testuser")
        assert retrieved is not None
        assert retrieved["username"] == "testuser"

    def test_sql_injection_attempt_negative(self):
        malicious_input = "admin' OR '1'='1"
        result = self.service.get_user_by_username(malicious_input)
        assert result is None

    def test_sql_injection_union_negative(self):
        malicious_input = "admin' UNION SELECT * FROM users--"
        result = self.service.get_user_by_username(malicious_input)
        assert result is None

    def test_sql_injection_comment_negative(self):
        malicious_input = "admin'--"
        result = self.service.get_user_by_username(malicious_input)
        assert result is None

    def test_empty_username_negative(self):
        with pytest.raises(ValueError, match="Username must be a non-empty string"):
            self.service.get_user_by_username("")

    def test_invalid_type_username_negative(self):
        with pytest.raises(ValueError, match="Username must be a non-empty string"):
            self.service.get_user_by_username(None)

    def test_duplicate_username_negative(self):
        self.service.create_user("unique_user", "email@example.com")
        with pytest.raises(ValueError, match="already exists"):
            self.service.create_user("unique_user", "another@example.com")
