from django.urls import path

from quizz.views import QuizzTemplateView, QuizzCreateView, QuizzListView, QuizzEditView, QuizzVisualisationFormView, QuizzImportMoodle
from quizz.views.quizz import export_quizz, delete_quizz

urlpatterns = [
    path('', QuizzTemplateView.as_view(), name="home"),
    path('quizz/add/', QuizzCreateView.as_view(), name="add_quizz"),
    path('quizz/<int:pk>/edit', QuizzEditView.as_view(), name="edit_quizz"),
    path('quizz/<int:pk>/test', QuizzVisualisationFormView.as_view(), name="visual_quizz"),
    path('quizz/list/', QuizzListView.as_view(), name="list_quizz"),
    path('download/<int:pk>', export_quizz, name="download"),
    path('delete/<int:pk>', delete_quizz, name="delete"),
    path('import/quizz/', QuizzImportMoodle.as_view(), name="import_moodle_quizz"),
]
