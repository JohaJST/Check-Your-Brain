from django.urls import path
from core.views import index, new_test, create_test
from core.auth import sign_in, sign_out

urlpatterns = [
    path("", index, name="home"),
    path("login", sign_in, name="login"),
    path("logout/", sign_out, name="logout"),
    path("test/new/", new_test, name="new_test"),
    path("test/create/", create_test, name="create_test")
]
