from django.urls import path

from quizz.views import QuizzTemplateView

urlpatterns = [
    path('', QuizzTemplateView.as_view(), name="home"),
]
