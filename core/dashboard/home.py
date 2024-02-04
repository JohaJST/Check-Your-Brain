from django.shortcuts import redirect, render


def home(requests):
    if requests.user.is_admin:
        return render(requests, 'pages/dashboard/index.html')
    else:
        return redirect("home")
