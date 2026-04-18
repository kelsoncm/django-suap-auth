import secrets

from django.core.exceptions import ImproperlyConfigured

# Default mapping: user model field → SUAP response key.
# A tuple key means "split the SUAP value on the first space and assign
# the first part to key[0] and the remainder to key[1]".
DEFAULT_USER_ATTR_MAP = {
    "username": "identificacao",
    "email": "email",
    ("first_name", "last_name"): "nome_usual",
}


def get_suap_settings():
    """Read and validate SUAP settings from Django settings.

    Expects a single SUAP_AUTH dictionary with all configuration:

    SUAP_AUTH = {
        'CLIENT_ID': 'your-id',
        'CLIENT_SECRET': 'your-secret',
        'REDIRECT_URI': 'https://example.com/callback/',
        'BASE_URL': 'https://suap.ifrn.edu.br',  # optional
        'SCOPES': ['identificacao', 'email'],  # optional
        'USER_LOOKUP_FIELD': 'username',  # optional
        'USER_ATTR_MAP': {...},  # optional
        'USER_JSON_FIELD': None,  # optional
        'DIRECT_REDIRECT': True,  # optional
    }
    """
    from django.conf import settings

    suap_auth = getattr(settings, "SUAP_AUTH", {})

    # Validate required fields
    required = ['CLIENT_ID', 'CLIENT_SECRET', 'REDIRECT_URI']
    missing = [field for field in required if not suap_auth.get(field)]

    if missing:
        raise ImproperlyConfigured(
            f"Missing required SUAP_AUTH settings: {', '.join(missing)}. "
            f"Configure SUAP_AUTH dictionary in settings.py"
        )

    return {
        "client_id": suap_auth["CLIENT_ID"],
        "client_secret": suap_auth["CLIENT_SECRET"],
        "redirect_uri": suap_auth["REDIRECT_URI"],
        "scopes": suap_auth.get("SCOPES", ["identificacao", "email"]),
        "base_url": suap_auth.get("BASE_URL", "https://suap.ifrn.edu.br"),
        "user_lookup_field": suap_auth.get("USER_LOOKUP_FIELD", "username"),
        "user_attr_map": suap_auth.get("USER_ATTR_MAP", DEFAULT_USER_ATTR_MAP),
        "json_field": suap_auth.get("USER_JSON_FIELD", None),
        "direct_redirect": suap_auth.get("DIRECT_REDIRECT", True),
    }


def _extract_nested(data, dotted_key):
    """Extract a value from a (possibly nested) dict using a dotted key path.

    Example: _extract_nested(data, "dados_pessoais.data_nascimento")
    """
    keys = dotted_key.split(".")
    value = data
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
        if value is None:
            return None
    return value


def apply_user_attr_map(user_info, attr_map):
    """Translate a SUAP user_info dict into a flat dict of user model field→value pairs.

    The ``attr_map`` uses the convention ``{model_field: suap_key}``:

    - **Plain string key**: maps the SUAP field to the given user model field.
    - **Tuple key** ``(field_a, field_b)``: splits the SUAP value on the first space;
      the part before the space goes to ``field_a`` and everything after to ``field_b``.
    - **Dotted SUAP key** (e.g. ``"dados_pessoais.data_nascimento"``): traverses nested
      dicts in the SUAP response.
    - Special key ``"fulljson"``: maps the entire raw SUAP response dict to the field.
      Suitable for a ``JSONField`` or any field that accepts a dict.
    - If the SUAP value is ``None`` or absent, the field is skipped.
    """
    result = {}
    for model_field, suap_key in attr_map.items():
        if suap_key == "fulljson":
            result[model_field] = user_info
            continue
        value = _extract_nested(user_info, suap_key)
        if value is None:
            continue
        if isinstance(model_field, (list, tuple)) and len(model_field) == 2:
            field_a, field_b = model_field
            parts = str(value).split(" ", 1)
            result[field_a] = parts[0]
            result[field_b] = parts[1] if len(parts) > 1 else ""
        else:
            result[model_field] = value
    return result


def get_oauth2_client():
    """Return a SuapOAuth2Client configured from Django settings."""
    from .client import SuapOAuth2Client

    cfg = get_suap_settings()
    return SuapOAuth2Client(
        client_id=cfg["client_id"],
        client_secret=cfg["client_secret"],
        redirect_uri=cfg["redirect_uri"],
        scopes=cfg["scopes"],
        base_url=cfg["base_url"],
    )


def generate_state():
    """Generate a cryptographically secure random state token for OAuth2 CSRF protection."""
    return secrets.token_urlsafe(32)
