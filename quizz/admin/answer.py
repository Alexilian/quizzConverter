from django.contrib import admin

from quizz.models import Answer


class AnswerAdmin(admin.ModelAdmin):

    list_display = ("question", "answer", "is_correct", "points")


admin.site.register(Answer, AnswerAdmin)
