from django.shortcuts import render, redirect
from core.models import Test, ClassRooms, Subject, ClassRoomsSubjects


def action(request, status, path, pk=None):
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
                    classrooms = ClassRooms.objects.all()
                    subjects = Subject.objects.all()
                    return render(request, "pages/dashboard/new.html",
                                  {"classrooms": classrooms, "subjects": subjects, "action": "test"})
                elif request.method == "POST":
                    return redirect("/dashboard/")
            elif path == "subject":
                if request.method == "GET":
                    classrooms = ClassRooms.objects.all()
                    return render(request, "pages/dashboard/new.html", {"action": "subject", "classrooms": classrooms})
                elif request.method == "POST":
                    subject = Subject.objects.create(name=request.POST.get("subject_name"))
                    subject.save()
                    classroom_id = 0
                    while f'classroom_{classroom_id}' in request.POST:
                        clsb = ClassRoomsSubjects.objects.create(classroom_id=ClassRooms.objects.get(id=request.POST.get(f'classroom_{classroom_id}')).id, subject_id=subject.id)
                        clsb.save()
                        classroom_id += 1
                    return redirect("/dashboard/list/subject/")
            elif path == "classroom":
                if request.method == "GET":
                    return render(request, "pages/dashboard/new.html", {"action": "classroom"})
                elif request.method == "POST":
                    class_room = ClassRooms.objects.create(name=request.POST.get("classroom_name"))
                    class_room.save()
                    return redirect("/dashboard/list/classroom/")
            return redirect("dlist", tip=path)
        else:
            return redirect("dlist", tip=path)
    else:
        return redirect("home")



