from django.contrib import admin
from core.models import User, ClassRooms, Subject, Variant,   Question, Test

# Register your models here.

admin.site.register(User)
admin.site.register(ClassRooms)
admin.site.register(Subject)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Variant)
