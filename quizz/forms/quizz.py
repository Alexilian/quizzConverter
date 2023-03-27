from django import forms
from django.forms import ModelForm

from quizz.models import Quizz, QuizzType


class QuizzForm(ModelForm):
    class Meta:
        model = Quizz
        fields = ["quizz_type", "title", "description"]