# Instalação

## Requisitos

- Python 3.10+
- Django 5.2+

## Instalar do PyPI

```bash
pip install django-suap-auth
```

## Adicionar a INSTALLED_APPS

```python
INSTALLED_APPS = [
    ...
    "django_suap_auth",
]
```

## Configurar URLs

```python
# urls.py
from django.urls import path, include

urlpatterns = [
    path("auth/suap/", include("django_suap_auth.urls")),
]
```
