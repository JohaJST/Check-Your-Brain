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
    # try:
    question = Question.objects.filter(test_id=test_id)
    print(question)
    variant = Variant.objects.all()
    print(variant)
    answer = Variant.objects.filter(is_answer=True)
    print(answer)
    ctx = {"question": question,
           "answer": answer,
           "variant": variant
           }
    # except:
    #     return redirect("home")
    return render(request, 'test.html', ctx)
