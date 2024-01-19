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
        print(request.POST)
        test_name = request.POST.get('test_name', "")
        print(test_name)
        if request.POST.get("test_name", ""):
            test = Test.objects.create(name=request.POST.get('test_name'))
            question_counter = 1
            while f'question_{question_counter}' in request.POST:
                question_text = request.POST[f'question_{question_counter}']
                question = Question.objects.create(text=question_text, test=test)

                variant_counter = 1
                while f'variant_{question_counter}_{variant_counter}' in request.POST:
                    variant_text = request.POST[f'variant_{question_counter}_{variant_counter}']
                    is_answer = f'answer_{question_counter}_{variant_counter}' in request.POST
                    Variant.objects.create(text=variant_text, is_answer=is_answer, question=question)

                    variant_counter += 1

                question_counter += 1

            return redirect('/')
        else:
            print("error")
    return redirect("/")
