from django import forms
from django.forms import ModelForm

from quizz.models import Quizz, QuizzType


class QuizzForm(ModelForm):
    class Meta:
        model = Quizz
        fields = ["title", "tags"]

    def custom_save(self):
        my_obj = self.save()
        return my_obj
