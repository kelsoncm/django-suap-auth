# django-suap-auth

Django OAuth2 authentication backend for **SUAP** (Sistema Unificado de Administração Pública), the academic management system of IFRN.

## Features

- OAuth2 authorization code flow with SUAP
- Configurable scopes (`identificacao`, `email`, `documentos_pessoais`, `dados_academicos`, `dados_pessoais`, `reitoria`)
- Flexible attribute mapping from SUAP response to Django user model fields
- Optional JSON field storage for the full SUAP response
- Configurable intermediate login page (`SUAP_AUTH_DIRECT_REDIRECT`)
- CSRF protection via state parameter validation

## Quick Links

- [Installation](installation.md)
- [Configuration](configuration.md)
- [Scopes](scopes.md)
- [Attribute Mapping](attribute-mapping.md)
