from django.urls import path
from core.views import index
from core.auth import sign_in, regis

urlpatterns = [
    path("", index, name="home"),
    path("login", sign_in, name="login"),
    path("regis/", regis, name="regis"),
]
