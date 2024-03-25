from django.urls import path
from core.quiz import index, new_test, create_test, user_profile, test, test_answer
from core.auth import sign_in, sign_out
from .dashboard import dlist, home, action, form, locked
from .quiz.index import required

urlpatterns = [
    path("", index, name="home"),
    path("login/", sign_in, name="login"),
    path("logout/", sign_out, name="logout"),
    path("user/", user_profile, name="user_profile"),
    path("test/<int:test_id>/", test, name="test"),
    path("test/answer/", test_answer, name="test_answer"),
    path("test/new/", new_test, name="new_test"),
    path("test/create/", create_test, name="create_test"),
    path("dashboard/", home, name="dashboard"),
    path("dashboard/list/<str:tip>/", dlist, name="dlist"),
    path("action/<str:status>/<str:path>/<int:pk>/", action, name='action'),
    path("action/<str:status>/<str:path>/", action, name='action_no_pk'),
    path("subject/<int:pk>/", index, name="sub"),
    path("form/user/", form, name="userform"),
    path("dashboard/locked/", locked, name="locked"),
    path("required/", required, name="required"),
    # path("dashboard/classRooms/<st:str>/", classroom, name="classroom"),
    # path("dashboard/subject/<st:str>/", subject, name="subject"),
    # path("dashboard/classRooms/<st:str>/<pk:int>/", classroom, name="classroom"),
    # path("dashboard/subject/<st:str>/<pk:int>/", subject, name="subject"),
]
