from django.conf import settings

from core.admin import userJust


def APP_NAME(request):
    userJust()
    return {"APP_NAME": settings.APP_NAME}
