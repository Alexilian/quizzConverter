from django.views.generic import TemplateView, FormView

from quizz.forms.quizz import QuizzForm
from quizz.models import QuizzType


class QuizzTemplateView(TemplateView):

    template_name = "quizz/home.html"


class QuizzCreateView(FormView):

    template_name = "quizz/create_quizz.html"
    form_class = QuizzForm

    def get_context_data(self, **kwargs):
        context = super(QuizzCreateView, self).get_context_data(**kwargs)
        context["quizz_type_list"] = QuizzType
        context["question_type_list"] = ("", "Vrai/Faux", "Choix multiple", "Choix unique")

        return context

