from django.urls import path

from quizz.views import QuizzTemplateView, QuizzCreateView, QuizzEditView

urlpatterns = [
    path('', QuizzTemplateView.as_view(), name="home"),
    path('quizz/add/', QuizzCreateView.as_view(), name="add_quizz"),
    #path('quizz/<int:pk>/', QuizzDetailView.as_view(), name="detail_quizz"),
    path('quizz/<int:pk>/edit', QuizzEditView.as_view(), name="edit_quizz"),
]
