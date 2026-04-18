from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    suap_auth = getattr(settings, "SUAP_AUTH", {})
    context = {
        "suap_client_id": suap_auth.get("CLIENT_ID", ""),
        "suap_redirect_uri": suap_auth.get("REDIRECT_URI", ""),
    }
    return render(request, "home/home.html", context)


@login_required
def dashboard(request):
    return render(request, "home/dashboard.html", {"user": request.user})
