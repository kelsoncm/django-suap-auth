from django.urls import include, path

urlpatterns = [
    path("auth/suap/", include("django_suap_auth.urls")),
    path("", include("home.urls")),
]
