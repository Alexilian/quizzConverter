from django import forms
from django.forms import ModelForm

from quizz.models import Quizz, QuizzType


class ImportMoodle(forms.Form):
    importXML = forms.FileField(label="Import XML Moodle", required=False)
    importAMC = forms.FileField(label="Import TEX AMC",  required=False)


