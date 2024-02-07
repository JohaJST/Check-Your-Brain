from django.shortcuts import redirect, render

from core.models import Test, Result, User, Subject


def home(requests):
    if requests.user.is_admin:
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
        return render(requests, 'pages/dashboard/index.html', {"qlen": len(q), "rlen": tmp, "ulen": len(u), "slen": len(s)})
    else:
        return redirect("home")
