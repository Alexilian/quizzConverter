from django.contrib import admin

from quizz.models import Quizz


class QuizzAdmin(admin.ModelAdmin):

    list_display = ("pk", "owner", "title", "tags")


admin.site.register(Quizz, QuizzAdmin)
