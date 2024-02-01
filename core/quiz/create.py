from django.shortcuts import render, redirect
from core.models import ClassRooms, Subject, Question, Variant, Test


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


def subject(request, st, pk=None):
    if st == "list":
        subjects = Subject.objects.all()
        return render(request, 'pages/dashboard/list.html', {"name": "Subject", "root": subjects})

def classroom(request, st, pk=None):
    pass