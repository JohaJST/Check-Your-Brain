from contextlib import closing

from django.contrib.auth.decorators import login_required
from django.db import connection
from django.shortcuts import redirect, render
from methodism import dictfetchall, dictfetchone

from core.models import Result, Subject, Test, User


@login_required(login_url="login")
def home(requests, classroom_id=None, status="subject", subject_id=None, user_id=None):
    if requests.user.in_dashboard:
        if status == "subject":
            sql = """SELECT cs.id, cs.name, SUM(cr."result")*100/SUM(cr.totalQuestions) as "foyiz" FROM core_subject cs
                    INNER join core_result cr on ct.subject_id == cs.id
                    inner join core_test ct ON cr.test_id == ct.id
                    GROUP by cs.id
                """
        elif status == "classroom":
            sql = f"""
                SELECT cc.id, cc.name, SUM(cr."result")*100/SUM(cr.totalQuestions) as "foyiz" FROM core_classrooms cc
                inner join core_user cu ON cc.id == cu.classroom_id
                INNER join core_result cr on cr.user_id  == cu.id
                inner join core_classroomssubjects cc2 on cc2.classroom_id == cc.id
                WHERE cc2.subject_id == {subject_id}
                GROUP by cc.id
            """
            requests.user.log["subject_id"] = subject_id
            requests.user.save()
        elif status == "user":
            sql = f"""
                SELECT cu.classroom_id, cu.id, cu.name, SUM(cr."result")*100/SUM(cr.totalQuestions) as "foyiz" FROM core_result cr
                inner join core_user cu on cr.user_id == cu.id
                INNER join core_test ct on ct.id == cr.test_id
                WHERE cu.classroom_id == {int(subject_id)} and ct.subject_id == {int(requests.user.log["subject_id"])}
                GROUP by cu.id
            """
        # print(sql)
        elif status == "result":
            sql = f"""
                    SELECT
                    cu.name, cu.last_name, cr.*, ct.name as "testname", cs.name as "cname", cc.name as "classroomname"
                    FROM core_result cr
                    inner join core_test ct ON
                    ct.subject_id == {int(requests.user.log["subject_id"])} and
                    cr.test_id == ct.id
                    inner join core_user cu ON cr.user_id == cu.id
                    inner join core_classrooms cc on cu.classroom_id == cc.id
                    INNER join core_subject cs on cs.id == ct.subject_id
                    WHERE cr.user_id == {user_id}
            """
        else:
            return redirect("dashboard")
        with closing(connection.cursor()) as cursor:
            cursor.execute(sql)
            result = dictfetchall(cursor)
        # print(result)
        # result.update({'sid': subject_id and 0})
        return render(
            requests, "pages/dashboard/index.html", {"result": result, "status": status}
        )
    else:
        return redirect("lock")


# @login_required(login_url="login")
def locked(request):
    # print(1)
    if request.method == "POST":
        # s
        # print(11)
        request.user.in_dashboard = request.user.check_password(
            request.POST.get("pass")
        )
        request.user.save()
        # print(12)
        return redirect("dashboard")
    if not request.user.is_admin:
        print(22)
        return redirect("home")
    print(3)
    return render(request, "pages/auth/login.html")


@login_required(login_url="login")
def lock(request):
    # print(1)
    if request.method == "POST":
        # s
        # print(11)
        request.user.in_dashboard = request.user.check_password(
            request.POST.get("pass")
        )
        request.user.save()
        # print(12)
        return redirect("dashboard")
    if not request.user.is_admin:
        # print(22)
        return redirect("home")
    # print(3)
    return render(request, "pages/dashboard/pass.html")
