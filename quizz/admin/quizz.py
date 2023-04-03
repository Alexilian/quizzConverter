from django.contrib import admin

from quizz.models import Quizz


class QuizzAdmin(admin.ModelAdmin):

    list_display = ("owner", "title", "description")


admin.site.register(Quizz, QuizzAdmin)
