from contextlib import closing

from django.contrib.auth.decorators import login_required
from django.db import connection
from django.shortcuts import redirect, render
from methodism import dictfetchone, dictfetchall

from core.models import Test, Result, User, Subject


@login_required(login_url="login")
def home(requests, status="subject"):
    if requests.user.in_dashboard:
        if status == "subject":
            sql = """SELECT cs.id, cs.name, SUM(cr."result")*100/SUM(cr.totalQuestions) as "foyiz" FROM core_subject cs 
                    INNER join core_result cr on ct.subject_id == cs.id
                    inner join core_test ct ON cr.test_id == ct.id 
                    GROUP by cs.id
                """

            with closing(connection.cursor()) as cursor:
                cursor.execute(sql)
                result = dictfetchall(cursor)
        print(result)
        return render(requests, "pages/dashboard/index.html", {'result': result, "a": "Test Result"})
    else:
        return redirect("locked")


@login_required(login_url="login")
def locked(request):
    if request.method == "POST":
        # s

        request.user.in_dashboard = request.user.check_password(request.POST.get("pass"))
        request.user.save()
        return redirect("dashboard")
    elif not request.user.is_admin:
        return redirect("home")
    return render(request, "pages/dashboard/pass.html")
