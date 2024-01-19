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
    print("1")
    if request.method == "POST":
        data = request.POST
        print(data)
    return redirect("/")
