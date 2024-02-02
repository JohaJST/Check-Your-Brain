from django.shortcuts import render

from core.models import Subject, ClassRooms, Variant, Result, User


def dlist(request, tip=None):
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
    return render(request, 'pages/dashboard/list.html')

