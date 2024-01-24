from django.conf import settings


def APP_NAME(request):
    return {"APP_NAME": settings.APP_NAME}
