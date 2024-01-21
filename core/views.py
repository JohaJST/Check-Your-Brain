from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from core.models import *


@login_required(login_url="login")
def index(request):
    return render(request, 'index.html')


def new_test(request):
    class_rooms = ClassRooms.objects.all()
    subjects = Subject.objects.all()
    return render(request, "new.html", {"classrooms": class_rooms, "subjects": subjects})


def create_test(request):
    if request.method == 'POST':
        subject = Subject.objects.get(id=request.POST.get('subject'))
        test_name = Test.objects.create(name=request.POST.get('test_name'), subject_id=subject)
        question_counter = 1
        while f'question_{question_counter}' in request.POST:
            question_text = request.POST[f'question_{question_counter}']
            question = Question.objects.create(text=question_text, test_id=test_name)

            variant_counter = 1
            while f'variant_{question_counter}_{variant_counter}' in request.POST:
                variant_text = request.POST[f'variant_{question_counter}_{variant_counter}']
                is_answer = f'answer_{question_counter}_{variant_counter}' in request.POST
                Variant.objects.create(text=variant_text, is_answer=is_answer, question_id=question)

                variant_counter += 1

            question_counter += 1

        return redirect('/')
    return redirect("/")
