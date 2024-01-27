from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from core.models import *
from core.models.test import Result


@login_required(login_url="login")
def index(request):
    subjects = Subject.objects.all()
    test_list = []
    is_subject = True
    if request.GET.get("is_subject") == "false":
        is_subject = False
        for test_ in Test.objects.all():
            if test_.subject == Subject.objects.get(id=request.GET.get("subject")):
                test_list.append(test_)
    return render(request, 'index.html', {'subjects': subjects, "tests": test_list, "is_subject": is_subject})



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


def new_test(request):
    is_subject = request.GET.get("is_subject")
    class_rooms = ClassRooms.objects.all()
    subjects = Subject.objects.all()
    return render(request, "new.html", {"classrooms": class_rooms, "subjects": subjects})


def create_test(request):
    if request.method == 'POST':
        classroom = ClassRooms.objects.get(id=request.POST.get('classroom'))
        subject = Subject.objects.get(id=request.POST.get('subject'))
        test_name = Test.objects.create(name=request.POST.get('test_name'), classroom=classroom, subject=subject)
        question_counter = 1
        while f'question_{question_counter}' in request.POST:
            question_text = request.POST[f'question_{question_counter}']
            question = Question.objects.create(text=question_text, test=test_name)

            variant_counter = 1
            while f'variant_{question_counter}_{variant_counter}' in request.POST:
                variant_text = request.POST[f'variant_{question_counter}_{variant_counter}']
                is_answer = f'answer_{question_counter}_{variant_counter}' in request.POST
                Variant.objects.create(text=variant_text, is_answer=is_answer, question=question)

                variant_counter += 1

            question_counter += 1

        return redirect('/')
    return redirect("/")


def user_profile(request):
    current_user = request.user
    results = Result.objects.all()
    results_list = []
    average = 0
    tmp = 0
    for result in results:
        if result.user == current_user:
            results_list.append(result)
            average += result.result
            tmp += 1

    ctx = {"user": current_user, "results": results, "average": average/tmp}
    return render(request, "profile.html", ctx)


def test_answer(request):
    current_user = request.user
    test_ = Test.objects.get(id=request.POST.get('test_id'))
    ctx = {"user": current_user, "test": test_}
    return render(request, "answer.html", ctx)
