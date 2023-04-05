from django.urls import path

from quizz.views import QuizzTemplateView, QuizzCreateView, QuizzImportMoodle

urlpatterns = [
    path('', QuizzTemplateView.as_view(), name="home"),
    path('add/quizz/', QuizzCreateView.as_view(), name="add_quizz"),
    path('import/quizz/', QuizzImportMoodle.as_view(), name="import_moodle_quizz"),
]
