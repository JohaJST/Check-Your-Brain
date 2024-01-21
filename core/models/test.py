from django.db import models
from core.models.classrooms import Subject


class Test(models.Model):
    name = models.TextField(default="", blank=True)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True, editable=False)

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.TextField()
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True, editable=False)

    def __str__(self):
        return self.text


class Variant(models.Model):
    text = models.TextField()
    is_answer = models.BooleanField(default=False)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True, editable=False)

    def __str__(self):
        return f"{self.question_id.test_id} {self.text} {self.question_id}"
