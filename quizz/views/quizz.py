from xml.etree import ElementTree as ET
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, FormView
from quizz.forms.importMoodle import ImportMoodle
from quizz.forms.quizz import QuizzForm
from quizz.models import Question, Quizz, Answer, QuestionType
import re


class QuizzTemplateView(TemplateView):

    template_name = "quizz/home.html"
def remove_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def read_XML(file_name):
    file = ET.parse(file_name).getroot()

    all = []

    try:
        quizz = Quizz(
            title = file_name
        )
        quizz.save()
        all.append(quizz)

        for question in file.findall('question'):
            newQuestion = None
            typeOfQuestion = question.attrib['type']
            questionText = question.find('questiontext')
            points = question.find('defaultgrade')
            answers = question.findall('answer')
            intituleQuestion = ""

            if questionText is not None:
                testquest = questionText.find("text")
                if testquest is not None:
                    intituleQuestion = remove_tags(testquest.text)

            if points is not None:
                newQuestion= Question(
                    title=intituleQuestion,
                    position =0,
                    comment =None,
                    type_of_question =typeOfQuestion,
                    quizz =quizz,
                    points =points.text,
                )
                newQuestion.save()
                all.append(newQuestion)

            newAnswer = None
            answerString = ""
            for answer in answers:
                answerText = answer.find('text')
                if answerText is not None:
                    if typeOfQuestion == "shortanswer":
                        answerString += remove_tags(answerText.text)
                    elif answer.attrib['fraction'] != "0":
                        newAnswer = Answer(
                            question= newQuestion,
                            answer = remove_tags(answerText.text),
                            is_correct = True,
                            points = int(answer.attrib['fraction'])/100
                        )
                        newAnswer.save()
                        all.append(newAnswer)
                    else:
                        newAnswer = Answer(
                            question=newQuestion,
                            answer=remove_tags(answerText.text),
                            points=int(answer.attrib['fraction'])/100
                        )
                        newAnswer.save()
                        all.append(newAnswer)

            if newAnswer is None:
                newAnswer = Answer(
                    question=newQuestion,
                    answer=answerString,
                    is_correct = True,
                    points=1
                )
                newAnswer.save()
                all.append(newAnswer)

    except Exception as e :
        print(e)
        for objet in all:
            objet.delete()




class QuizzImportMoodle(FormView):
    template_name = "quizz/importFromMoodle.html"
    form_class = ImportMoodle

    def get_success_url(self):
        return reverse("home")
    def form_valid(self, form):
        file = form.cleaned_data["importXML"]
        read_XML(file)
        return super(QuizzImportMoodle, self).form_valid(form)
    def form_invalid(self, form):
        print(form.errors)
        return super(QuizzImportMoodle, self).form_invalid(form)





class QuizzCreateView(CreateView):

    template_name = "quizz/create_quizz.html"
    form_class = QuizzForm

    def get_success_url(self):
        return reverse('home')

    def get_context_data(self, **kwargs):
        context = super(QuizzCreateView, self).get_context_data(**kwargs)
        context["question_type_list"] = QuestionType

        return context

    def form_valid(self, form):

        list_question = {}
        created_objects = []

        try:

            new_quizz = form.custom_save()
            """new_quizz = Quizz(
                title=self.request.POST["title"],
                description=self.request.POST["description"]
            )
            new_quizz.save()"""
            created_objects.append(new_quizz)

            for key in list(self.request.POST.keys())[3:]:

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

                the_type = the_question["type_question"]
                the_title = the_question["title"]
                the_comment = the_question["comment"]
                the_point = the_question["point"]
                if the_type not in ["Réponse libre", "Réponse libre justification image"]:
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
            for the_object in created_objects:
                the_object.delete()
            return super(QuizzCreateView, self).form_invalid(form)


class QuizzEditView(CreateView):

    template_name = "quizz/edit_quizz.html"
    form_class = QuizzForm

    def get_success_url(self):
        return reverse('home')

    def get_context_data(self, **kwargs):
        context = super(QuizzEditView, self).get_context_data(**kwargs)
        the_quizz = Quizz.objects.get(pk=self.kwargs["pk"])
        all_questions = Question.objects.filter(quizz=the_quizz)
        all_answers = []
        for question in list(all_questions):
            if Answer.objects.filter(question=question).count() > 0:
                all_answers.extend(list(Answer.objects.filter(question=question)))
        context["question_type_list"] = QuestionType
        context["the_quizz"] = the_quizz
        context["all_questions"] = all_questions
        context["all_answers"] = all_answers

        return context

    def form_valid(self, form):

        list_question = {}
        created_objects = []

        try:

            new_quizz = form.custom_save()
            created_objects.append(new_quizz)

            for key in list(self.request.POST.keys())[3:]:

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

                the_type = the_question["type_question"]
                the_title = the_question["title"]
                the_comment = the_question["comment"]
                the_point = the_question["point"]
                if the_type not in ["Réponse libre", "Réponse libre justification image"]:
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
            Quizz.objects.get(pk=self.kwargs["pk"]).delete()
            return super(QuizzEditView, self).form_valid(form)

        except Exception as e:
            print(e)
            for the_object in created_objects:
                the_object.delete()
            return super(QuizzEditView, self).form_invalid(form)
