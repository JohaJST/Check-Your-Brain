from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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
        print(data)
        return redirect("home")
    subjects = Subject.objects.all()
    tests = Test.objects.all()
    questions = Question.objects.all()
    variants = Variant.objects.all()
    ctx = {"subjects": subjects, "tests": tests, "questions": questions, "variants": variants}
    return render(request, 'test.html', ctx)


