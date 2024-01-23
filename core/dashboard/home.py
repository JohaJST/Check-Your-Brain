from django.shortcuts import redirect, render


def home(requests):
    return render(requests, 'pages/dashboard/index.html')
