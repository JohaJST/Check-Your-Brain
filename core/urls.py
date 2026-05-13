from django.urls import path

from core.auth import sign_in, sign_out
from core.quiz import create_test, index, new_test, test, test_answer, user_profile

from .dashboard import action, dlist, form, home, lock, locked
from .quiz.index import required

urlpatterns = [
    path("", index, name="home"),
    path("login/", sign_in, name="login"),
    path("logout/", sign_out, name="logout"),
    path("user/", user_profile, name="user_profile"),
    path("test/<int:test_id>/", test, name="test"),  # github test
    path("test/answer/", test_answer, name="test_answer"),
    path("test/new/", new_test, name="new_test"),
    path("test/create/", create_test, name="create_test"),
    path("dashboard/", home, name="dashboard"),
    path("dashboard/<str:status>/", home, name="dashboard_subject"),
    path("dashboard/<str:status>/<int:subject_id>/", home, name="dashboard_classroom"),
    path("dashboard/<str:status>/<int:classroom_id>/", home, name="dashboard_user"),
    path(
        "dashboard/<str:status>/<int:classroom_id>/<int:user_id>/",
        home,
        name="dashboard_result",
    ),
    path("dashboard/list/<str:tip>/", dlist, name="dlist"),
    path("action/<str:status>/<str:path>/<int:pk>/", action, name="action"),
    path("action/<str:status>/<str:path>/", action, name="action_no_pk"),
    path("subject/<int:pk>/", index, name="sub"),
    path("form/user/", form, name="userform"),
    path("dashboard/lockedd/", required, name="lockedd"),
    path("locked/", lock, name="lock"),
    path("required/", required, name="required"),
    # path("dashboard/classRooms/<st:str>/", classroom, name="classroom"),
    # path("dashboard/subject/<st:str>/", subject, name="subject"),
    # path("dashboard/classRooms/<st:str>/<pk:int>/", classroom, name="classroom"),
    # path("dashboard/subject/<st:str>/<pk:int>/", subject, name="subject"),
]
