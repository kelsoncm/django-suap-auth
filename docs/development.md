# Development

## Setup

```bash
git clone https://github.com/kelsoncm/django-suap-auth.git
cd django-suap-auth
pip install -e ".[dev]"
pre-commit install
pre-commit install --hook-type pre-push
```

## Running Tests

```bash
pytest --cov=django_suap_auth --cov-report=term-missing
```

## Code Style

```bash
ruff check .
ruff format .
```

## pre-commit

The project uses pre-commit hooks:
- **pre-commit**: trailing whitespace, end of file fixer, yaml check, ruff lint/format
- **pre-push**: pytest

## Documentation

```bash
mkdocs serve
```
