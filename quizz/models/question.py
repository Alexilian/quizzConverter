from django.db import models

from quizz.models.quizz import Quizz


class QuestionType(models.TextChoices):
    Libre = "Réponse libre"
    ImageJustif = "Réponse libre justification image"
    Boolean = "Vrai/Faux"
    Multiple = "Choix multiple"
    Unique = "Choix unique"


class Question(models.Model):
    title = models.CharField(max_length=255)
    position = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    type_of_question = models.CharField(max_length=255, blank=True, null=True)
    quizz = models.ForeignKey(Quizz, on_delete=models.CASCADE, related_name="questions", null=True, blank=True)
    points = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_xml_question_type(self):
        if self.type_of_question == 'multiple_choice':
            return 'multichoice'
        if self.type_of_question == 'true_false':
            return 'truefalse'
        if self.type_of_question == 'single_choice':
            return 'multichoice'
        return self.type_of_question
