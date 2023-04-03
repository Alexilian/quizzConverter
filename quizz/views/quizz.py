from django.urls import reverse
from django.views.generic import TemplateView, FormView

from quizz.forms.quizz import QuizzForm
from quizz.models import QuizzType, Question, Quizz, Answer

import re


class QuizzTemplateView(TemplateView):

    template_name = "quizz/home.html"


class QuizzCreateView(FormView):

    template_name = "quizz/create_quizz.html"
    form_class = QuizzForm

    def get_success_url(self):
        return reverse('home')

    def get_context_data(self, **kwargs):
        context = super(QuizzCreateView, self).get_context_data(**kwargs)
        context["question_type_list"] = ("", "Vrai/Faux", "Choix multiple", "Choix unique")

        return context

    def form_valid(self, form):

        list_question = {}
        created_objects = []

        try:

            new_quizz = Quizz(
                quizz_type=self.request.POST["quizz_type"],
                title=self.request.POST["title"],
                description=self.request.POST["description"]
            )
            new_quizz.save()
            created_objects.append(new_quizz)
            for key in list(self.request.POST.keys())[4:]:

                id_q = re.findall(r'\d+', key)
                if len(id_q) == 1:
                    id_q = id_q[0]
                    if "type_question_" in key:
                        if id_q in list_question:
                            list_question[id_q]["type_question"] = self.request.POST[key]
                        else:
                            list_question[id_q] = {"type_question": self.request.POST[key]}
                    elif "title_" in key:
                        if id_q in list_question:
                            list_question[id_q]["title"] = self.request.POST[key]
                        else:
                            list_question[id_q] = {"title": self.request.POST[key]}
                    elif "comment_" in key:
                        if id_q in list_question:
                            list_question[id_q]["comment"] = self.request.POST[key]
                        else:
                            list_question[id_q] = {"comment": self.request.POST[key]}
                    elif "point_" in key:
                        if id_q in list_question:
                            list_question[id_q]["point"] = self.request.POST[key]
                        else:
                            list_question[id_q] = {"point": self.request.POST[key]}
                elif len(id_q) == 2:
                    if "answers" not in list_question[id_q[0]]:
                        list_question[id_q[0]]["answers"] = {}
                    if list_question[id_q[0]]["type_question"] == "Vrai/Faux" and "q_"+id_q[0]+"_answer_"+id_q[1] == key:
                        list_question[id_q[0]]["answers"] = self.request.POST[key]
                    elif list_question[id_q[0]]["type_question"] == "Choix multiple":
                        if id_q[1] not in list_question[id_q[0]]["answers"]:
                            list_question[id_q[0]]["answers"][id_q[1]] = {"point": None, "answer": None}
                        if "point_"+id_q[0]+"_answer_"+id_q[1] == key:
                            list_question[id_q[0]]["answers"][id_q[1]]["point"] = self.request.POST[key]
                        elif "q_"+id_q[0]+"_answer_"+id_q[1] == key:
                            list_question[id_q[0]]["answers"][id_q[1]]["answer"] = self.request.POST[key]
                    elif list_question[id_q[0]]["type_question"] == "Choix unique":
                        if id_q[1] not in list_question[id_q[0]]["answers"]:
                            list_question[id_q[0]]["answers"][id_q[1]] = {"point": None, "answer": None}
                        if "q_"+id_q[0]+"_answer_"+id_q[1] == key:
                            list_question[id_q[0]]["answers"][id_q[1]]["answer"] = self.request.POST[key]
                            if id_q[0] == 1:
                                list_question[id_q[0]]["answers"][id_q[1]]["point"] = 1
                            else:
                                list_question[id_q[0]]["answers"][id_q[1]]["point"] = 0

            for question_number in list(list_question):
                the_question = list_question[question_number]

                print("Salut a tous", the_question)

                the_type = the_question["type_question"]
                the_title = the_question["title"]
                the_comment = the_question["comment"]
                the_point = the_question["point"]
                the_answers = the_question["answers"]
                new_question = Question(
                    title=the_title,
                    comment=the_comment,
                    type_of_question=the_type,
                    quizz=new_quizz,
                    points=float(the_point),
                )
                new_question.save()
                created_objects.append(new_question)

                if the_type == "Vrai/Faux":
                    new_answer = Answer(
                        answer=the_answers,
                        question=new_question,
                        is_correct=the_answers,
                        points=100
                    )
                    new_answer.save()
                    created_objects.append(new_answer)

                elif the_type == "Choix unique":
                    for the_answer in list(the_answers):
                        if the_answer == 0:
                            new_answer = Answer(
                                 answer=the_answers[the_answer]["answer"],
                                 question=new_question,
                                 is_correct=True,
                                 points=100
                            )
                            new_answer.save()
                            created_objects.append(new_answer)
                        else:
                            new_answer = Answer(
                                answer=the_answers[the_answer]["answer"],
                                question=new_question,
                                is_correct=False,
                                points=0
                            )
                            new_answer.save()
                            created_objects.append(new_answer)

                elif the_type == "Choix multiple":
                    for the_answer in list(the_answers):
                        new_answer = Answer(
                            answer=the_answers[the_answer]["answer"],
                            question=new_question,
                            is_correct=True if float(the_answers[the_answer]["point"]) > 0 else False,
                            points=float(the_answers[the_answer]["point"])
                        )
                        new_answer.save()
                        created_objects.append(new_answer)

            return super(QuizzCreateView, self).form_valid(form)

        except Exception as e:
            print(e)

            return super(QuizzCreateView, self).form_invalid(form)
