from django.shortcuts import render, redirect
from core.models import Subject, ClassRooms, Variant, Result, User, Test, Question


def dlist(request, tip=None):
    if request.user.is_admin:
        if tip == "subject":
            subjects = Subject.objects.all()
            return render(request, 'pages/dashboard/list.html', {"name": "Subject", "root": subjects})
        elif tip == "classroom":
            cr = ClassRooms.objects.all()
            return render(request, 'pages/dashboard/list.html', {"name": "ClassRoom", "root": cr})
        elif tip == "result":
            result = Result.objects.all()
            return render(request, 'pages/dashboard/list.html', {"name": "Result", "root": result})
        elif tip == "user":
            return render(request, 'pages/dashboard/list.html', {"name": "User", "root": User.objects.all()})
        elif tip == "quiz":
            return render(request, 'pages/dashboard/list.html', {"name": "Quiz", "root": Test.objects.all()})
        elif tip == "variant":
            return render(request, 'pages/dashboard/list.html', {"name": "Variant", "root": Variant.objects.all()})
        elif tip == "question":
            return render(request, 'pages/dashboard/list.html', {"name": "Question", "root": Question.objects.all()})
        elif tip == "new":
            return render(request, 'pages/dashboard/new.html', {"subjects": Subject.objects.all(), "classrooms": ClassRooms.objects.all()})
        return render(request, 'pages/dashboard/list.html')
    else:
        return redirect('home')
