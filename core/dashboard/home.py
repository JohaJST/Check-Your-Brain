from django.shortcuts import redirect, render

from core.models import Test


def home(requests):
    if requests.user.is_admin:
        q = Test.objects.all()
        return render(requests, 'pages/dashboard/index.html', {"qlen": len(q)})
    else:
        return redirect("home")
