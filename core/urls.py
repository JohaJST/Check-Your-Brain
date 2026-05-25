from django.urls import path
from core.auth import sign_in, sign_out
from .dashboard import action, dlist, form, home
from core.quiz import index, new_test, create_test, user_profile, test, test_answer, test_result

urlpatterns = [
    path("", index, name="home"),
    path("login/", sign_in, name="login"),
    path("logout/", sign_out, name="logout"),
    path("user/", user_profile, name="user_profile"),
    path("test/<int:test_id>/", test, name="test"),
    path("test/<int:test_id>/result/", test_result, name="test_result"),   # ← NEW
    path("test/answer/", test_answer, name="test_answer"),
    path("test/new/", new_test, name="new_test"),
    path("test/create/", create_test, name="create_test"),
    path("dashboard/", home, name="dashboard"),
    path("dashboard/list/<str:tip>/", dlist, name="dlist"),
    path("action/<str:status>/<str:path>/<int:pk>/", action, name='action'),
    path("action/<str:status>/<str:path>/", action, name='action_no_pk'),
    path("subject/<int:pk>/", index, name="sub"),
    path("form/user/", form, name="userform"),
]
