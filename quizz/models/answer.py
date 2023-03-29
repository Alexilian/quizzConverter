from django.db import models

from quizz.models.question import Question


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers", null=True, blank=True)
    answer = models.CharField(max_length=255, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    points = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.answer
