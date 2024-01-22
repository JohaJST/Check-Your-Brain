from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from core.models.classrooms import ClassRooms


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, is_staff=False, is_superuser=False, **extra_fields):
        user = self.model(username=username, is_staff=is_staff, is_superuser=is_superuser,
                          **extra_fields)
        if password is not None:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        return self.create_user(username, password, is_staff=True, is_superuser=True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=256, null=True, unique=True)
    name = models.CharField(max_length=256, null=True)
    classroom = models.ForeignKey(ClassRooms, on_delete=models.SET_NULL, null=True, blank=True)

    log = models.JSONField(default={'state': 0})
    lang = models.CharField(default='uz', max_length=2, choices=[("uz", 'uz'), ("ru", 'ru'), ("en", 'en'), ])
    ut = models.SmallIntegerField(verbose_name="User Type", default=3, choices=[
        (1, 'Admin'),
        (2, "Teacher"),
        (3, "User"),
    ])  # user type

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, editable=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['ut']

    class Meta:
        verbose_name_plural = "1. Users"

    def full_name(self):
        return f"{self.name}"

    def personal(self):
        ut = {
            1: 'Admin',
            2: "Teacher",
            3: "User",
        }[self.ut]

        return {
            'username': self.username,
            'name': self.name,
            'lang': self.lang,
            'user_type': ut,
            "ClassRoom": self.classroom,
            "created": self.created,
            "updated": self.updated
        }

    def __str__(self):
        return f"{self.id} || {self.full_name()} || {self.username}"


class Otp(models.Model):
    key = models.CharField(max_length=512)
    username = models.CharField(max_length=20)
    is_expired = models.BooleanField(default=False)
    tries = models.SmallIntegerField(default=0)
    extra = models.JSONField(default=dict({}))
    is_verified = models.BooleanField(default=False)
    step = models.CharField(max_length=25)

    created = models.DateTimeField(auto_now=False, auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def save(self, *args, **kwargs):
        if self.tries >= 3:
            self.is_expired = True
        if self.is_verified:
            self.is_expired = True
        return super(Otp, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} -> {self.key}"

    class Meta:
        verbose_name_plural = "8. One Time Password"


class TG_User(models.Model):
    user_id = models.BigIntegerField(unique=True)
    phone = models.CharField('Phone', unique=True, max_length=50)
    username = models.CharField(max_length=128)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    classroom = models.ForeignKey(ClassRooms, on_delete=models.SET_NULL, null=True, blank=True)

    log = models.JSONField(default={'state': 0})
    lang = models.CharField(default='uz', max_length=2, choices=[("uz", 'uz'), ("ru", 'ru'), ("en", 'en'), ])
    ut = models.SmallIntegerField(verbose_name="User Type", default=3, choices=[
        (1, 'Admin'),
        (2, "Teacher"),
        (3, "User"),
    ])  # user type
    is_admin = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, editable=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

    class Meta:
        verbose_name_plural = "0. TG_Users"

    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    def tg_user_format(self):
        ut = {
            1: 'Admin',
            2: "Teacher",
            3: "User",
        }[self.ut]
        return {
            "tg_user_id": self.user_id,
            'mobile': self.phone,
            'username': self.username,
            "ClassRoom": self.classroom,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'lang': self.lang,
            "log": self.log,
            'user_type': ut,
            "created": self.created,
            "updated": self.updated
        }

    def __str__(self):
        return f"{self.full_name()} || {self.phone}"
