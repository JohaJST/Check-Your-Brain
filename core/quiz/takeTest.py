from contextlib import closing

from django.contrib.auth.decorators import login_required
from django.db import connection
from django.shortcuts import render, redirect
from django.views.generic import View
from methodism import dictfetchall, dictfetchone

from core.models import Test, Question, Variant, Subject, Result


@login_required(login_url="login")
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
        sql = f"SELECT count(*) from core_question q where q.test_id = {test_id}"
        with closing(connection.cursor()) as cursor:
            cursor.execute(sql)
            totalQuestion = dictfetchone(cursor)
        # print(totalQuestion)
        foyiz = int(data["result"]) * 100 / totalQuestion["count(*)"]
        Result.objects.create(test_id=test_id, user=request.user, result=int(data["result"]), foyiz=foyiz, totalQuestions=totalQuestion["count(*)"])
        return redirect("home")
    try:
        question = Question.objects.filter(test_id=test_id)
    # print(question)
        variant = Variant.objects.all()

    # print(variant)
    # answer = Variant.objects.filter(is_answer=True)
    # print(answer)
        ctx = {"question": question,
               # "answer": answer,
               "variant": variant,
               "test": Test.objects.get(id=test_id)
               }
    except:
        return redirect("home")
    #     return redirect("home")
    return render(request, 'test.html', ctx)



