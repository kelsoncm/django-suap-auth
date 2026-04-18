from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    context = {
        "suap_client_id": settings.SUAP_CLIENT_ID,
        "suap_redirect_uri": settings.SUAP_REDIRECT_URI,
    }
    return render(request, "home/home.html", context)


@login_required
def dashboard(request):
    return render(request, "home/dashboard.html", {"user": request.user})
