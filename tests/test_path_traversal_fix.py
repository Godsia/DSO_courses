import tempfile
from pathlib import Path

import pytest

from src.app.path_traversal_fix import FileService


class TestPathTraversalFix:

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.service = FileService(self.temp_dir)
        
        (Path(self.temp_dir) / "test.txt").write_text("test content")
        (Path(self.temp_dir) / "subdir").mkdir()
        (Path(self.temp_dir) / "subdir" / "nested.txt").write_text("nested content")

    def teardown_method(self):
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_read_file_positive(self):
        content = self.service.read_file("test.txt")
        assert content == "test content"

    def test_read_nested_file_positive(self):
        content = self.service.read_file("subdir/nested.txt")
        assert content == "nested content"

    def test_path_traversal_dot_dot_negative(self):
        with pytest.raises(ValueError, match="Path traversal detected"):
            self.service.read_file("../../etc/passwd")

    def test_path_traversal_absolute_negative(self):
        with pytest.raises(ValueError, match="Path traversal detected"):
            self.service.read_file("/etc/passwd")

    def test_path_traversal_encoded_negative(self):
        with pytest.raises(ValueError, match="Path traversal detected"):
            self.service.read_file("..%2F..%2Fetc%2Fpasswd")

    def test_path_traversal_multiple_dots_negative(self):
        with pytest.raises(ValueError, match="Path traversal detected"):
            self.service.read_file("../../../etc/passwd")

    def test_path_traversal_mixed_negative(self):
        with pytest.raises(ValueError, match="Path traversal detected"):
            self.service.read_file("subdir/../../etc/passwd")

    def test_empty_path_negative(self):
        with pytest.raises(ValueError, match="File path must be a non-empty string"):
            self.service.read_file("")

    def test_invalid_type_negative(self):
        with pytest.raises(ValueError, match="File path must be a non-empty string"):
            self.service.read_file(None)

    def test_nonexistent_file_negative(self):
        result = self.service.read_file("nonexistent.txt")
        assert result is None
