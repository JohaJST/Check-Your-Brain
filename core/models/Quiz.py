from django.db import models

from core.models import User
from core.models.classrooms import Subject


class Tests(models.Model):
    name = models.CharField(max_length=256)
    timeout = models.IntegerField("Testlarni ishlashga beriladigan vaqt", default=40)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    created = models.DateField(auto_now_add=True, auto_now=False, null=True)
    updated = models.DateField(auto_now_add=False, auto_now=True, null=True)

    def __str__(self):
        return f"{self.name}  ||  {self.subject}  ||  {self.created}"

    def test_format(self):
        return {
            self.name,
            self.created,
            self.updated
        }

    class Meta:
        verbose_name_plural = "T. Test"


class Quiz(models.Model):
    name = models.CharField(max_length=1028)
    img = models.ImageField(blank=True, null=True)
    desc = models.TextField(null=True, blank=True)
    ball = models.IntegerField()
    test = models.ForeignKey(Tests, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True, editable=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name}  ||  {self.test.subject}  || Ball: {self.ball}"

    def test_format(self):
        return {
            self.name,
            self.img,
            self.desc,
            self.ball,
            self.subject,
            self.created,
            self.updated
        }

    class Meta:
        verbose_name_plural = "4. Tests"


class Variant(models.Model):
    answer = models.CharField(max_length=218)
    is_true = models.BooleanField(default=False)
    test = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True, editable=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.test.name}  ||  {self.answer}  ||  {self.is_true}"

    def variant_format(self):
        return {
            self.answer,
            self.is_true,
            self.test,
            self.updated,
            self.created
        }

    class Meta:
        verbose_name_plural = "6. Variants"


class CompletedTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    test = models.ForeignKey(Quiz, on_delete=models.SET_NULL, blank=True, null=True)
    is_true = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True, editable=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.test.name}  ||  {self.user.full_name()}  ||  {self.is_true}"

    def comp_test_forma(self):
        return {
            self.user.full_name(),
            self.test.name,
            self.is_true,
            self.created,
            self.updated
        }

    class Meta:
        verbose_name_plural = "5. Completed Tests"


class AllTests(models.Model):
    Subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    test = models.ForeignKey(Tests, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    all_balls = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True, editable=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user}  ||  {self.Subject.name}  ||  {self.all_balls}"

    def all_test_forma(self):
        return {
            self.user.full_name(),
            self.Subject.name,
            self.all_balls,
            self.created,
            self.updated
        }

    class Meta:
        verbose_name_plural = "7. All Tests"
