from django.contrib.auth.models import User
from django.db import models


class QuizzType(models.TextChoices):
    MOODLE = "moodle", "Moodle"
    AMC = "amc", "AMC"


class Quizz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzes", null=True, blank=True)
    title = models.CharField(max_length=40)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # plural
    class Meta:
        verbose_name_plural = "Quizzes"
