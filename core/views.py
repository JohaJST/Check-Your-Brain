from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from core.models import *


@login_required(login_url="login")
def index(request):
    subjects = Subject.objects.all()
    return render(request, 'index.html', {'subjects': subjects})


def test(request):
    subjects = Subject.objects.all()
    tests = Test.objects.all()
    return render(request, 'test.html', {subjects: subjects, tests: tests, })


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
    return render(request, "profile.html", {"user": current_user})
