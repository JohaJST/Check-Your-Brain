import datetime
import random

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from methodism import code_decoder

from core.models import User, Otp, ClassRooms
from methodism import generate_key
import uuid


def sign_in(requests):
    if not requests.user.is_anonymous:
        return redirect("home")

    if requests.POST:
        data = requests.POST
        user = User.objects.filter(phone=data['phone']).first()

        if not user:
            return render(requests, 'pages/auth/login.html', {"error": "Phone xato"})

        if not user.check_password(data['pass']):
            return render(requests, 'pages/auth/login.html', {"error": "Parol xato"})

        if not user.is_active:
            return render(requests, 'pages/auth/login.html', {"error": "Profil active emas "})
        login(requests, user)
        return redirect('home')

    return render(requests, 'pages/auth/login.html')


# def regis(request):
#     c = ClassRooms.objects.all()
#     if not request.user.is_anonymous:
#         return redirect('home')
#     if request.POST:
#         data = request.POST
#         # print(data)
#         nott = "phone" if "phone" not in data\
#             else "firstname" if "first_name" not in data\
#             else "lastname" if "last_name" not in data\
#             else "password" if "pass" not in data\
#             else "password-conf" if "pass-conf" not in data\
#             else "sinf" if "sinf" not in data else ""
#
#         if nott:
#             return render(request, "pages/auth/regis.html", {
#                 "error": f"{nott} datada bo'lishi kere",
#                 "sinf": c
#             })
#
#         user = User.objects.filter(phone=data["phone"]).first()
#
#         if user:
#             return render(request, "pages/auth/regis.html", {
#                 "error": "Bu nomer band",
#                 "sinf": c
#             })
#
#         if data["pass"] != data["pass-conf"]:
#             return render(request, "pages/auth/regis.html", {
#                 "error": "Parol bir biri bilan mos emas",
#                 "sinf": c
#             })
#
#         sinf = ClassRooms.objects.filter(name=data["sinf"]).first()
#
#         if not sinf:
#             return render(request, "pages/auth/regis.html", {
#                 "error": "Sinf topilmadi",
#                 "sinf": c
#             })
#
#         user_new = User.objects.create_user(phone=data["phone"], password=data["pass"], **data)
#         authenticate(user_new)
#         return redirect('home')
#
#
#     # print(">>>>>>", c)
#
#     return render(request, "pages/auth/regis.html", {"sinf": c})

# def otp(request):
#     if not request.session.get("otp_token"):
#         return redirect("login")
#
#     if request.POST:
#         otp = Otp.objects.filter(key=request.session["otp_token"]).first()
#         code = request.POST['code']
#
#         if not code.isdigit():
#             return render(request, "pages/auth/otp.html", {"error": "Harflar kiritmang!!!"})
#
#         if otp.is_expired:
#             otp.step = "failed"
#             otp.save()
#             return render(request, "pages/auth/otp.html", {"error": "Token eskirgan!!!"})
#
#         if (datetime.datetime.now() - otp.created).total_seconds() >= 120:
#             otp.is_expired = True
#             otp.save()
#             return render(request, "pages/auth/otp.html", {"error": "Vaqt tugadi!!!"})
#         unhashed = code_decoder(otp.key, decode=True, l=settings.RANGE)
#         unhash_code = eval(settings.UNHASH)
#         if int(unhash_code) != int(code):
#             otp.tries += 1
#             otp.save()
#             return render(request, "pages/auth/otp.html", {"error": "Cod hato!!!"})
#
#         user = User.objects.get(phone=request.session["phone"])
#         otp.step = "logged"
#         login(request, user)
#         otp.save()
#
#         del request.session["user_id"]
#         del request.session["code"]
#         del request.session["phone"]
#         del request.session["otp_token"]
#
#         return redirect("home")
#
#     return render(request, "pages/auth/otp.html")


# def resent_otp(request):
#     if not request.session.get("otp_token"):
#         return redirect("login")
#
#     old = Otp.objects.filter(key=request.session["otp_token"]).first()
#     old.step = 'failed'
#     old.is_expired = True
#     old.save()
#
#     otp = random.randint(int(f'1{"0" * (settings.RANGE - 1)}'), int('9' * settings.RANGE))
#     # shu yerda sms chiqib ketadi
#     code = eval(settings.CUSTOM_HASHING)
#     hash = code_decoder(code, l=settings.RANGE)
#     token = Otp.objects.create(key=hash, mobile=old.mobile, step='login', extra={"via": "template"})
#
#     request.session['otp_token'] = token.key
#     request.session['code'] = otp
#     request.session['phone'] = token.mobile
#
#     return redirect("otp")


@login_required(login_url='login')
def sign_out(request):
    logout(request)
    return redirect("login")
