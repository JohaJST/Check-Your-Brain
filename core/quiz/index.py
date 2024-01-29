from contextlib import closing

from django.contrib.auth.decorators import login_required
from django.db import connection
from django.shortcuts import render, redirect
from methodism import dictfetchone, dictfetchall

from core.models import Subject, Result, Test


@login_required(login_url="login")
def index(request):
    sql = f"""
    SELECT s.id, s.name
    FROM core_classroomssubjects cs
    INNER JOIN core_subject s ON cs.subject_id = s.id
    WHERE cs.classroom_id = {request.user.classroom_id}
    group by s.id 
    """
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        subjects = dictfetchall(cursor)
    # print(subjects)
    # subjects = Subject.objects.all()
    # print("1")
    if request.GET.get("is_subject") == "false":
        tests = Test.objects.filter(subject_id=request.GET.get("subject"))
        # print(tests)
        # print("11")
        return render(request, 'index.html', {'tests': tests})
    # print("2")
    # print(subjects)
    return render(request, 'index.html', {'subjects': subjects,  "is_subject": True})


@login_required(login_url="login")
def user_profile(request):
    current_user = request.user
    results = Result.objects.all()
    results_list = []
    average = 0
    tmp = 0
    for result in results:
        if result.user == current_user:
            results_list.append(result)
            average += result.result
            tmp += 1

    ctx = {"user": current_user, "results": results, "average": average/tmp}
    return render(request, "profile.html", ctx)
