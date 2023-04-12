from django.urls import path

from quizz.views import QuizzTemplateView, QuizzCreateView, QuizzListView

urlpatterns = [
    path('', QuizzTemplateView.as_view(), name="home"),
    path('add/quizz/', QuizzCreateView.as_view(), name="add_quizz"),
    path('ListQuizz/', QuizzListView.as_view(), name="list_quizz"),
]
