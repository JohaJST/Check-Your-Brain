from django.db import models

from core.models import ClassRooms, Subject, User


class Test(models.Model):
    name = models.CharField(max_length=256)
    desc = models.TextField(null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    is_start = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.desc is None:
            self.desc = " "
        return super(Test, self).save(*args, **kwargs)


class Question(models.Model):
    text = models.TextField(null=True, blank=True)
    img = models.ImageField(null=True, blank=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True, editable=False)

    def __str__(self):
        return self.text


class Variant(models.Model):
    text = models.TextField()
    is_answer = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True, editable=False)

    def __str__(self):
        return f"{self.question.test} {self.text} {self.question}"


class Result(models.Model):
    foyiz = models.IntegerField(null=True, blank=True)
    result = models.IntegerField(null=True)
    totalQuestions = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True, auto_now=False, null=True, blank=True, editable=False)

    def __str__(self):
        return f"{self.user} | {self.result} {self.test}"


class OldResult(models.Model):
    foyiz = models.IntegerField(null=True, blank=True)
    result = models.IntegerField(null=True)
    totalQuestions = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} || {self.result} || {self.test}"

    # def save(self, *args, **kwargs):
    #     self.foyiz = self.test.


class TestClassRoom(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRooms, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.test} | {self.classroom}"
