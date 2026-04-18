# Configuration

## Required Settings

```python
SUAP_CLIENT_ID = "your-client-id"
SUAP_CLIENT_SECRET = "your-client-secret"
SUAP_REDIRECT_URI = "https://yourapp.example.com/auth/suap/callback/"
```

## Optional Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `SUAP_BASE_URL` | `https://suap.ifrn.edu.br` | SUAP base URL |
| `SUAP_AUTH_SCOPES` | `["identificacao", "email"]` | OAuth2 scopes |
| `SUAP_USER_LOOKUP_FIELD` | `"username"` | Django user field used for lookup |
| `SUAP_USER_ATTR_MAP` | See below | Mapping from user model fields to SUAP response keys |
| `SUAP_USER_JSON_FIELD` | `None` | Field to store the full SUAP JSON response |
| `SUAP_AUTH_DIRECT_REDIRECT` | `True` | Redirect directly to SUAP (`True`) or show intermediate page (`False`) |

## Authentication Backend

```python
AUTHENTICATION_BACKENDS = [
    "django_suap_auth.backends.SuapAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
]
```
