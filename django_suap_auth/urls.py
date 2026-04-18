from django.urls import path

from .views import SuapCallbackView, SuapLoginView, SuapDebugView

app_name = "suap_auth"

urlpatterns = [
    path("login/", SuapLoginView.as_view(), name="login"),
    path("callback/", SuapCallbackView.as_view(), name="callback"),
    path("debug/", SuapDebugView.as_view(), name="debug"),
]
