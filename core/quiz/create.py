from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from core.models import ClassRooms, Subject, Question, Variant, Test, TestClassRoom


@login_required(login_url="login")
def new_test(request):
    is_subject = request.GET.get("is_subject")
    class_rooms = ClassRooms.objects.all()
    subjects = Subject.objects.all()
    return render(request, "pages/dashboard/new.html", {"classrooms": class_rooms, "subjects": subjects})


@login_required(login_url="login")
def create_test(request):
    if request.method == 'POST':
        subject = Subject.objects.get(id=request.POST.get('subject'))
        test_name = Test.objects.create(name=request.POST.get('test_name'), subject=subject)
        question_counter = 1
        try:
            tscr = TestClassRoom.objects.create(test_id=test_name.id, classroom_id=ClassRooms.objects.get(id=request.POST.get('classroom_1')).id)
            tscr.create()
            tscr = TestClassRoom.objects.create(test_id=test_name.id, classroom_id=ClassRooms.objects.get(id=request.POST.get('classroom_2')).id)
            tscr.create()
            tscr = TestClassRoom.objects.create(test_id=test_name.id, classroom_id=ClassRooms.objects.get(id=request.POST.get('classroom_3')).id)
            tscr.create()
            tscr = TestClassRoom.objects.create(test_id=test_name.id, classroom_id=ClassRooms.objects.get(id=request.POST.get('classroom_4')).id)
            tscr.create()
        except:
            print(123)
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

        return redirect('dashboard')
    return redirect("dashboard")

