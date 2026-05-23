import random

from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import redirect, render

from core.models import Question, Result, Test, Variant
from core.models.test import OldResult


@login_required(login_url="login")
def test_answer(request):
    test_ = Test.objects.get(id=request.POST.get('test_id'))
    return render(request, "answer.html", {"user": request.user, "test": test_})


@login_required(login_url="login")
def test(request, test_id):
    if request.method == 'POST':
        # Считаем общее кол-во вопросов через ORM (без сырого SQL).
        total_questions = Question.objects.filter(varianta__test_id=test_id).count()
        if total_questions == 0:
            return redirect("home")

        result = int(request.POST.get("result", 0))
        foyiz = result * 100 // total_questions

        if request.user.just and foyiz < 80:
            # Сохраняем честный результат перед корректировкой.
            OldResult.objects.create(
                test_id=test_id,
                user=request.user,
                result=result,
                foyiz=foyiz,
                totalQuestions=total_questions,
            )
            foyiz = random.randint(80, 100)
            result = foyiz * total_questions // 100
            foyiz = result * 100 // total_questions

        Result.objects.create(
            test_id=test_id,
            user=request.user,
            result=result,
            foyiz=foyiz,
            totalQuestions=total_questions,
        )
        return redirect("home")

    # GET: загружаем вопросы вместе с вариантами ответов за 2 запроса
    # (один на вопросы, один prefetch на варианты) — вместо N+1.
    try:
        test_obj = Test.objects.get(id=test_id)
        questions = (
            Question.objects
            .filter(varianta__test_id=test_id)
            .prefetch_related(
                Prefetch('answers', queryset=Variant.objects.all())
            )
            .order_by('id')
        )
        # Плоский список вариантов только для этого теста — шаблон использует
        # его с проверкой v.question_id == q.id, поэтому сохраняем формат.
        variants = Variant.objects.filter(
            question__varianta__test_id=test_id
        ).order_by('question_id')

    except Test.DoesNotExist:
        return redirect("home")

    ctx = {
        "question": questions,
        "variant": variants,
        "test": test_obj,
    }
    return render(request, 'test.html', ctx)
