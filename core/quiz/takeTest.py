from contextlib import closing

from django.contrib.auth.decorators import login_required
from django.db import connection
from django.shortcuts import render, redirect
from methodism import dictfetchall

from core.models import Test, Question, Variant, Subject


def test_answer(request):
    current_user = request.user
    test_ = Test.objects.get(id=request.POST.get('test_id'))
    ctx = {"user": current_user, "test": test_}
    return render(request, "answer.html", ctx)


@login_required(login_url="login")
def test(request, test_id):
    if request.POST:
        data = request.POST
        # print(data)
        return redirect("home")
    try:
        sql = """
            SELECT
                q.id AS question_id,
                q.text AS question_name,
                v.text AS variant_name,
                v.is_answer
            FROM
                core_question q
            JOIN
                core_variant v ON q.id = v.question_id
            WHERE
                q.test_id = 2;
        """
        # test = Test.objects.filter(id=test_id).first()
        with closing(connection.cursor()) as cursor:
            cursor.execute(sql)
            subjects = dictfetchall(cursor)
    except:
        return redirect("home")
    return render(request, 'test.html', {"all": sql})


