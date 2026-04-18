# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in django-suap-auth, please report it
by opening a [GitHub Security Advisory](https://github.com/kelsoncm/django-suap-auth/security/advisories/new).

**Please do not report security vulnerabilities through public GitHub issues.**

We will acknowledge your report within 48 hours and provide a more detailed
response within 7 days. If the issue is confirmed, we will release a patch as
soon as possible.

## Security Considerations

- OAuth2 state parameter is validated on every callback to prevent CSRF attacks.
- Access tokens are never stored; they are exchanged immediately for user info.
- Client secrets must be kept out of version control.
- Always use HTTPS in production (`SUAP_REDIRECT_URI` must use HTTPS in production).
