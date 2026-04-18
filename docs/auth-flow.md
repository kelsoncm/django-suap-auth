# Authentication Flow

## Overview

django-suap-auth implements the OAuth2 Authorization Code flow.

```
User → /auth/suap/login/ → SUAP authorization page
     ← redirect with code ←
User → /auth/suap/callback/?code=...&state=...
     → exchange code for token
     → fetch user info from SUAP /api/eu/
     → authenticate/create Django user
     → redirect to LOGIN_REDIRECT_URL
```

## Direct Redirect (Default)

With `SUAP_AUTH_DIRECT_REDIRECT = True` (default), the user is immediately redirected to SUAP when they visit `/auth/suap/login/`.

## Intermediate Page

With `SUAP_AUTH_DIRECT_REDIRECT = False`, the login view renders an intermediate page (`django_suap_auth/login.html`) where the user must click a button to proceed to SUAP.

## CSRF Protection

The state parameter is generated using `secrets.token_urlsafe(32)` and stored in the session. It is validated on the callback to prevent CSRF attacks.
