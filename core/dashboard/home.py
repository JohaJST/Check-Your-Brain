from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from core.models import Test, Result, User, Subject


@login_required(login_url="login")
def home(requests):
    if requests.user.in_dashboard:
        q = Test.objects.all()
        r = Result.objects.all()
        u = User.objects.all()
        s = Subject.objects.all()
        a = 0
        for i in r:
            a += int(i.foyiz)
        if a != 0:
            tmp = a // len(r)
        else:
            tmp = 100
        return render(requests, 'pages/dashboard/index.html',
                      {"qlen": len(q), "rlen": tmp, "ulen": len(u), "slen": len(s)})
    else:
        return redirect("locked")


@login_required(login_url="login")
def locked(request):
    if request.method == "POST":
        # shotta parol tekshirish kere
        # if request.POST.get("pass") == request.user.
        a = request.user.in_dashboard = True
        a.save()
        return redirect("dashboard")
    elif not request.user.is_admin:
        return redirect("home")
    return render(request, "pages/dashboard/pass.html")
