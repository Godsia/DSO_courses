from pathlib import Path
from typing import Optional


class FileService:

    def __init__(self, base_directory: str):
        self.base_dir = Path(base_directory).resolve()
        if not self.base_dir.exists():
            raise ValueError(f"Base directory does not exist: {base_directory}")
        if not self.base_dir.is_dir():
            raise ValueError(f"Base path is not a directory: {base_directory}")

    def _validate_path(self, file_path: str) -> Path:
        if not file_path or not isinstance(file_path, str):
            raise ValueError("File path must be a non-empty string")
        
        file_path = file_path.lstrip('/')
        
        resolved_path = (self.base_dir / file_path).resolve()
        
        try:
            resolved_path.relative_to(self.base_dir)
        except ValueError:
            raise ValueError(f"Path traversal detected: {file_path}")
        
        return resolved_path

    def read_file(self, file_path: str) -> Optional[str]:
        try:
            safe_path = self._validate_path(file_path)
            if not safe_path.exists() or not safe_path.is_file():
                return None
            return safe_path.read_text(encoding='utf-8')
        except (ValueError, OSError) as e:
            raise ValueError(f"Invalid file path: {e}")

    def file_exists(self, file_path: str) -> bool:
        try:
            safe_path = self._validate_path(file_path)
            return safe_path.exists() and safe_path.is_file()
        except ValueError:
            return False
