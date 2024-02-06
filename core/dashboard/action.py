from django.shortcuts import render, redirect
from core.models import Test, ClassRooms, Subject


def action(request, status, pk, path):
    if request.user.is_admin:
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
                    class_rooms = ClassRooms.objects.all()
                    subjects = Subject.objects.all()
                    return render(request, "pages/dashboard/new.html",
                                  {"classrooms": class_rooms, "subjects": subjects, "action": "test"})
                elif request.method == "POST":
                    return redirect()
            elif path == "subject":
                if request.method == "GET":
                    return render(request, "pages/dashboard/new.html", {"action": "subject"})
            elif path == "classroom":
                if request.method == "GET":
                    return render(request, "pages/dashboard/new.html", {"action": "classroom"})
            # elif path == "classroom_subject":
            #     if request.method == "GET":
            #         return render(request, "pages/dashboard/new.html", {"action": "classroom_subject"})
            return redirect("dlist", tip=path)
        else:
            return redirect("dlist", tip=path)
    else:
        return redirect("home")



