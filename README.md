# DSO Courses - P08 CI/CD

[![CI/CD](https://github.com/Godsia/DSO_courses/actions/workflows/ci.yml/badge.svg)](https://github.com/Godsia/DSO_courses/actions/workflows/ci.yml)

Repository for DSO course practices.

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment.

### Features

- ✅ Automated testing with pytest
- ✅ Code quality checks (ruff, black, isort)
- ✅ Coverage reports
- ✅ Artifact storage
- ✅ Staging deployment simulation

### Workflow

1. **Test and Lint** - Runs on every push and PR
   - Python 3.12
   - Linters: ruff, black, isort
   - Tests: pytest with coverage
   - Artifacts: test reports and coverage

2. **Deploy (Staging)** - Runs on push to main
   - Simulates deployment to staging environment
   - Creates deployment artifacts

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run linters
ruff check src/ tests/
black --check src/ tests/
isort --check-only src/ tests/

# Run tests
pytest -v
```
