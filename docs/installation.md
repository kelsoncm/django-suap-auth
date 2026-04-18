# Installation

## Requirements

- Python 3.10+
- Django 5.2+

## Install from PyPI

```bash
pip install django-suap-auth
```

## Add to INSTALLED_APPS

```python
INSTALLED_APPS = [
    ...
    "django_suap_auth",
]
```

## Configure URLs

```python
# urls.py
from django.urls import path, include

urlpatterns = [
    path("auth/suap/", include("django_suap_auth.urls")),
]
```
