from urllib.parse import urlsplit, urlunsplit

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View

from .exceptions import SuapStateMismatchError, SuapTokenError, SuapUserInfoError
from .utils import generate_state, get_oauth2_client, get_suap_settings


class SuapLoginView(View):
    """
    Initiates the SUAP OAuth2 authorization code flow.

    If ``SUAP_AUTH_DIRECT_REDIRECT`` is ``True`` (the default), the user is
    redirected immediately to SUAP. Set it to ``False`` to render an
    intermediate confirmation page instead — subclass this view and override
    ``get_intermediate_template`` to customize the template rendered.
    """

    intermediate_template = "django_suap_auth/login.html"

    def get(self, request):
        cfg = get_suap_settings()
        if not cfg["direct_redirect"]:
            from django.shortcuts import render
            return render(request, self.intermediate_template)

        client = get_oauth2_client()
        state = generate_state()
        request.session["suap_oauth2_state"] = state
        authorization_url = client.get_authorization_url(state)
        return redirect(authorization_url)

    def post(self, request):
        """Handle form submission from the intermediate login page."""
        client = get_oauth2_client()
        state = generate_state()
        request.session["suap_oauth2_state"] = state
        authorization_url = client.get_authorization_url(state)
        return redirect(authorization_url)


class SuapCallbackView(View):
    """Handles the OAuth2 callback from SUAP."""

    def get(self, request):
        from django.conf import settings

        error = request.GET.get("error")
        if error:
            messages.error(request, f"SUAP login error: {error}")
            return redirect(settings.LOGIN_URL)

        try:
            received_state = request.GET.get("state", "")
            stored_state = request.session.pop("suap_oauth2_state", None)
            if not stored_state or received_state != stored_state:
                raise SuapStateMismatchError("OAuth2 state mismatch — possible CSRF attack.")

            code = request.GET.get("code")
            client = get_oauth2_client()
            token_data = client.exchange_code_for_token(code)
            access_token = token_data.get("access_token")
            user_info = client.get_user_info(access_token)

            user = authenticate(request, suap_user_info=user_info)
            if user is not None:
                login(request, user, backend="django_suap_auth.backends.SuapAuthBackend")
                next_url = request.GET.get("next", "")
                safe_next_url = next_url.replace("\\", "")
                parsed_next = urlsplit(safe_next_url)
                is_safe = (
                    safe_next_url
                    and safe_next_url.startswith("/")
                    and not parsed_next.scheme
                    and not parsed_next.netloc
                    and url_has_allowed_host_and_scheme(
                        url=safe_next_url,
                        allowed_hosts={request.get_host()},
                        require_https=request.is_secure(),
                    )
                )
                if is_safe:
                    # Reconstruct a safe relative URL from only the validated path and
                    # query components, explicitly dropping scheme, netloc, and fragment.
                    safe_redirect = urlunsplit(("", "", parsed_next.path, parsed_next.query, ""))
                    return HttpResponseRedirect(safe_redirect)
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                messages.error(request, "Authentication failed. Please try again.")
                return redirect(settings.LOGIN_URL)

        except SuapStateMismatchError:
            messages.error(request, "Security check failed. Please try logging in again.")
            return redirect(settings.LOGIN_URL)
        except SuapTokenError:
            messages.error(request, "Failed to complete login. Please try again.")
            return redirect(settings.LOGIN_URL)
        except SuapUserInfoError:
            messages.error(request, "Failed to retrieve your profile. Please try again.")
            return redirect(settings.LOGIN_URL)
