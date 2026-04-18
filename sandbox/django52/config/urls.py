from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/suap/", include("django_suap_auth.urls")),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", include("home.urls")),
]
