# django-suap-auth

[![PyPI Version](https://img.shields.io/pypi/v/django-suap-auth)](https://pypi.org/project/django-suap-auth/)
[![Python Versions](https://img.shields.io/pypi/pyversions/django-suap-auth)](https://pypi.org/project/django-suap-auth/)
[![Django Versions](https://img.shields.io/badge/django-5.2%20|%206.0-blue)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/kelsoncm/django-suap-auth/actions/workflows/test.yml/badge.svg)](https://github.com/kelsoncm/django-suap-auth/actions/workflows/test.yml)
[![Coverage](https://codecov.io/gh/kelsoncm/django-suap-auth/branch/main/graph/badge.svg)](https://codecov.io/gh/kelsoncm/django-suap-auth)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

Django OAuth2 authentication backend for **SUAP** (Sistema Unificado de Administração Pública), the academic management system of [IFRN](https://www.ifrn.edu.br), hosted at [suap.ifrn.edu.br](https://suap.ifrn.edu.br).

## Installation

```bash
pip install django-suap-auth
```

## Quick Start

```python
# settings.py
INSTALLED_APPS = [
    ...
    "django_suap_auth",
]

AUTHENTICATION_BACKENDS = [
    "django_suap_auth.backends.SuapAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
]

SUAP_CLIENT_ID = "your-client-id"
SUAP_CLIENT_SECRET = "your-client-secret"
SUAP_REDIRECT_URI = "https://yourapp.example.com/auth/suap/callback/"
SUAP_AUTH_SCOPES = ["identificacao", "email"]  # optional
LOGIN_REDIRECT_URL = "/dashboard/"
LOGIN_URL = "/login/"
```

```python
# urls.py
from django.urls import path, include

urlpatterns = [
    path("auth/suap/", include("django_suap_auth.urls")),
    ...
]
```

```html
<!-- template -->
<a href="{% url 'suap_auth:login' %}">Login com SUAP</a>
```

## Available Scopes

| Scope | Description |
|-------|-------------|
| `identificacao` | Basic identification (matricula, name, campus) |
| `email` | Email address |
| `documentos_pessoais` | Personal documents (CPF, RG) |
| `dados_academicos` | Academic data (course, grades, situation) |
| `dados_pessoais` | Personal data (birth date, nationality) |
| `reitoria` | Institution-level data |

## Documentation

Full documentation is available in the [`docs/`](docs/) directory and at the project's GitHub Pages.

## License

MIT © 2026 kelsoncm
