from django.contrib import admin

from quizz.models import Quizz


class QuizzAdmin(admin.ModelAdmin):

    list_display = ("owner", "title", "description", "quizz_type")


admin.site.register(Quizz, QuizzAdmin)
