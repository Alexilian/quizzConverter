from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, FormView, ListView

from quizz.forms.importMoodle import ImportMoodle
from quizz.forms.quizz import QuizzForm
from quizz.models import Question, Quizz, Answer, QuestionType

from xml.etree import ElementTree as ET

import os
import re


class QuizzTemplateView(TemplateView):

    template_name = "quizz/home.html"


# Enleve les tag html sur les ligne
def remove_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


# Lis un xml moodle
def read_moodle(file_name):
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
            if typeOfQuestion == "shortanswer":
                typeOfQuestion = "Réponse libre"
            elif typeOfQuestion == "multichoice":
                typeOfQuestion = "Choix multiple"
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
                    if typeOfQuestion == "Réponse libre":
                        answerString += remove_tags(answerText.text) + ";"
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
                    answer=answerString[:-1],
                    is_correct=True,
                    points=1
                )
                newAnswer.save()
                all.append(newAnswer)

    except Exception as e :
        print(e)
        for objet in all:
            objet.delete()


# Pas encore fonctionnel mais import un fichier TEX
def import_from_tex(file_path):
    question_type = None
    with open(file_path, 'r') as f:
        content = f.read()

    # Split the content by questions
    question_strs = re.findall(r'\\begin{question}{.+?}(.*?)(?=\\begin{question}|\\end{document})', content, re.DOTALL)

    for question_str in question_strs:
        # Extract the title
        title_match = re.search(r'(?<=[\n\.])\s*([A-Z].*?\.)(?=\s)', question_str)
        print(title_match)
        if title_match:
            title = title_match.group(1).strip()
        else:
            title = ''

        # Extract the type of question
        type_of_question_match = re.search(r'\\begin{question}{(.+)}', question_str)
        if type_of_question_match:
            type_of_question = type_of_question_match.group(1)
            if type_of_question == 'truefalse':
                question_type = QuestionType.Boolean
            elif type_of_question == 'multiple':
                question_type = QuestionType.Multiple
            elif type_of_question == 'single':
                question_type = QuestionType.Unique
            elif type_of_question == 'freestyle':
                question_type = QuestionType.Libre
            elif type_of_question == 'freestylejimg':
                question_type = QuestionType.ImageJustif
            else:
                question_type = ''

        # Extract the answers
        answers = []
        answers_match = re.search(r'\\begin{reponses}(.*?)\\end{reponses}', question_str, re.DOTALL)
        if answers_match:
            answer_strs = re.findall(r'\\(wrongchoice|correctchoice)\[(\w)\](.*?)\n', answers_match.group(1))
            for answer_str in answer_strs:
                answer = answer_str[2].strip()
                is_correct = answer_str[0] == 'correctchoice'
                points = float(answer_str[1]) if answer_str[1] else None
                answers.append({'answer': answer, 'is_correct': is_correct, 'points': points})

        # Save the question and answers
        question = Question(title=title, type_of_question=question_type)
        for answer_data in answers:
            answer = Answer(question=question, **answer_data)

    return len(question_strs)


# sauvegarde le xml
def save_uploaded_file(uploaded_file):
    # Make sure the file is an InMemoryUploadedFile
    if not isinstance(uploaded_file, InMemoryUploadedFile):
        raise TypeError("Expected an InMemoryUploadedFile object")

    # Create a new file in write binary mode
    filename = uploaded_file.name
    filepath = os.path.join(filename)
    with open(filepath, "wb") as f:
        # Write the contents of the uploaded file to the new file
        for chunk in uploaded_file.chunks():
            f.write(chunk)

    # Return the path to the new file
    return filepath


# convertit en appelant les fonction du dessus
class QuizzImportMoodle(FormView):
    template_name = "quizz/importFromMoodle.html"
    form_class = ImportMoodle

    def get_success_url(self):
        return reverse("list_quizz")

    def form_valid(self, form):
        if form.cleaned_data["importXML"] is not None:
            fileMoodle = form.cleaned_data["importXML"]
            read_moodle(fileMoodle)
        elif form.cleaned_data["importAMC"] is not None:
            fileAMC = form.cleaned_data["importAMC"]
            fileSaved = save_uploaded_file(fileAMC)
            data = import_from_tex(fileSaved)
            print(data)
            # for question in questions:
            #     print(question.title, question.type_of_question)

            os.remove(fileSaved)
        return super(QuizzImportMoodle, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(QuizzImportMoodle, self).form_invalid(form)


# créer un quizz
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
                the_point = the_question["point"]
                if the_type not in ["Réponse libre", "Réponse libre justification image"]:
                    the_answers = the_question["answers"]
                new_question = Question(
                    title=the_title,
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
                        points=1
                    )
                    new_answer.save()
                    created_objects.append(new_answer)

                elif the_type == "Choix unique":
                    print(list(the_answers))
                    for the_answer in list(the_answers):
                        if the_answer == "1":
                            new_answer = Answer(
                                 answer=the_answers[the_answer]["answer"],
                                 question=new_question,
                                 is_correct=True,
                                 points=1
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


# edit un quizz
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
                the_point = the_question["point"]
                if the_type not in ["Réponse libre", "Réponse libre justification image"]:
                    the_answers = the_question["answers"]
                new_question = Question(
                    title=the_title,
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
                        points=1
                    )
                    new_answer.save()
                    created_objects.append(new_answer)

                elif the_type == "Choix unique":
                    for the_answer in list(the_answers):
                        if the_answer == "1":
                            new_answer = Answer(
                                 answer=the_answers[the_answer]["answer"],
                                 question=new_question,
                                 is_correct=True,
                                 points=1
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


# permet de visualiser le quizz
class QuizzVisualisationFormView(FormView):

    template_name = "quizz/visual_quizz.html"
    form_class = QuizzForm

    def get_context_data(self, **kwargs):
        context = super(QuizzVisualisationFormView, self).get_context_data(**kwargs)
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

        note = 0
        for question in context["all_questions"]:
            note += question.points
        context["note_max"] = int(note) if int(note) == note else note

        return context

    def post(self, request, **kwargs):
        point_totaux = 0
        point_attente = 0
        for element in self.request.POST.keys():
            if element[0] == "a":
                id = re.findall(r'\d+', element)[0]
                the_answer = Answer.objects.get(id=id)

                if the_answer.question.type_of_question == "Vrai/Faux":
                    if the_answer.answer == self.request.POST[element]:
                        point_totaux += the_answer.question.points * the_answer.points
                else:
                    point_totaux += the_answer.question.points * the_answer.points

            elif element[0] == "q":
                id = re.findall(r'\d+', element)[0]
                the_question = Question.objects.get(id=id)
                if the_question.type_of_question == "Réponse libre":
                    if Answer.objects.filter(question=the_question).count() == 0:
                        point_attente += the_question.points
                    elif self.request.POST[element] in Answer.objects.get(question=the_question).answer.split(";"):
                        point_totaux += Answer.objects.get(question=the_question).points * the_question.points
                else:
                    point_totaux += Answer.objects.get(id=self.request.POST[element]).points * the_question.points
            if self.get_context_data().get('note_max') == int(self.get_context_data().get('note_max')):
                point_totaux = int(point_totaux)
            if point_attente == int(point_attente):
                point_attente = int(point_attente)
        return render(request, "quizz/result_test.html", {"point_attente": point_attente, "point_totaux": point_totaux, "note_max": self.get_context_data().get('note_max')})


# affiche la liste des quizz
class QuizzListView(ListView):

    model = Quizz
    template_name = 'quizz/list_quizz.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request):
        object_list = Quizz.objects.filter(tags__icontains=self.request.POST["search"])
        return render(request, "quizz/list_quizz.html", {"object_list": object_list})


# export sous xml un quizz
def export_quizz(request, pk):
    quiz = Quizz.objects.get(pk=pk)
    root = ET.Element('quiz')
    tree = ET.ElementTree(root)
    ET.indent(root, space="\t", level=0)

    name = ET.SubElement(root, 'name')
    name.text = quiz.title

    for question in quiz.questions.all():
        q = ET.SubElement(root, 'question', {'type': question.get_xml_question_type()})

        question_text = ET.SubElement(q, 'questiontext', {'format': 'html'})
        text = ET.SubElement(question_text, 'text')
        text.text = question.title

        for answer in question.answers.all():
            a = ET.SubElement(q, 'answer', {'fraction': '100' if answer.is_correct else '0'})
            answer_text = ET.SubElement(a, 'text')
            answer_text.text = answer.answer

    # Generate the XML string
    xml_string = ET.tostring(root, encoding='utf-8')

    # Create an HTTP response with the XML content
    response = HttpResponse(xml_string, content_type='text/xml')
    response['Content-Disposition'] = 'attachment; filename="quiz.xml"'
    return response


# supprime un quizz
def delete_quizz(request, pk):
    Quizz.objects.get(pk=pk).delete()
    return redirect(reverse('list_quizz'), kwargs={'object_list': Quizz.objects.all()})
