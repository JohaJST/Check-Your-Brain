from django.shortcuts import render, redirect
from core.models import Test


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
        else:
            return redirect("dlist", tip=path)
    else:
        return redirect("home")
