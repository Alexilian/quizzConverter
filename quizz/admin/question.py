from django.contrib import admin

from quizz.models import Question


class QuestionAdmin(admin.ModelAdmin):

    list_display = ("position", "title", "comment", "type_of_question", "quizz", "points")


admin.site.register(Question, QuestionAdmin)
