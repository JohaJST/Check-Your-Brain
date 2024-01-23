from django.urls import path
from core.views import index, new_test, create_test, user_profile
from core.auth import sign_in, sign_out
from .dashboard.home import home

urlpatterns = [
    path("", index, name="home"),
    path("login", sign_in, name="login"),
    path("logout/", sign_out, name="logout"),
    path("user/", user_profile, name="user_profile"),
    path("test/new/", new_test, name="new_test"),
    path("test/create/", create_test, name="create_test"),
    path("dashboard/", home, name="dashboard")
]
