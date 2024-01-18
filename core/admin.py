from django.contrib import admin
from core.models import User, Otp, ClassRooms, AllTests, CompletedTest, Quiz, Subject, Variant, TG_User, Tests

# Register your models here.

admin.site.register(User)
admin.site.register(CompletedTest)
admin.site.register(Otp)
admin.site.register(ClassRooms)
admin.site.register(Subject)
admin.site.register(Variant)
admin.site.register(Quiz)
admin.site.register(AllTests)
admin.site.register(TG_User)
admin.site.register(Tests)
