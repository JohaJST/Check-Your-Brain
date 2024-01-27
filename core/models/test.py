from django.db import models

from core.models import ClassRooms, Subject, User


class Test(models.Model):
    name = models.CharField(max_length=256)
    desc = models.TextField(null=True, blank=True)
    classroom = models.ForeignKey(ClassRooms, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True, editable=False)

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     a = 0
    #     for i in Question.objects.get(test_id=self.id):
    #         a += 1
    #

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True, editable=False)

    def __str__(self):
        return f"{self.user} | {self.result} {self.test}"

    # def save(self, *args, **kwargs):
    #     self.foyiz = self.test.
