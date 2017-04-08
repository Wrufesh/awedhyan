import json
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView
from rest_framework.response import Response

from app.utils.utilities import base64_content_file
from .serializers import QuestionSerializer, TestSerializer, TestQuestionDetailSerializer
from app.utils.mixins import DeleteView, UpdateView, CreateView, LoginRequiredMixin
from .forms import BoardForm, FacultyForm, ProgramForm, ProgramLevelForm, InstituteForm, CourseForm, ChapterForm, \
    QuestionForm, OptionForm, TestCreateForm
from .models import BoardOrUniversity, Faculty, Program, ProgramLevel, Institute, Course, ChapterPage, Question, Option, \
    Test, TestQuestion

from django.views.generic import TemplateView

from app.apps.users.forms import InstituteUserForm

User = get_user_model()


class InstituteView(LoginRequiredMixin):
    model = Institute
    success_url = reverse_lazy('aadhyan:institute_list')
    form_class = InstituteForm


class InstituteList(InstituteView, ListView):
    pass


class InstituteCreate(InstituteView, CreateView):
    pass


class InstituteEdit(InstituteView, UpdateView):
    pass


class InstituteDelete(InstituteView, DeleteView):
    pass


class BoardView(LoginRequiredMixin):
    model = BoardOrUniversity
    success_url = reverse_lazy('aadhyan:board_list')
    form_class = BoardForm


class BoardList(BoardView, ListView):
    pass


class BoardCreate(BoardView, CreateView):
    pass


class BoardEdit(BoardView, UpdateView):
    pass


class BoardDelete(BoardView, DeleteView):
    pass


class FacultyView(LoginRequiredMixin):
    model = Faculty
    success_url = reverse_lazy('aadhyan:faculty_list')
    form_class = FacultyForm


class FacultyList(FacultyView, ListView):
    pass


class FacultyCreate(FacultyView, CreateView):
    pass


class FacultyEdit(FacultyView, UpdateView):
    pass


class FacultyDelete(FacultyView, DeleteView):
    pass


class ProgramView(LoginRequiredMixin):
    model = Program
    success_url = reverse_lazy('aadhyan:program_list')
    form_class = ProgramForm


class ProgramList(ProgramView, ListView):
    pass


class ProgramCreate(ProgramView, CreateView):
    pass


class ProgramEdit(ProgramView, UpdateView):
    pass


class ProgramDelete(ProgramView, DeleteView):
    pass


class ProgramLevelView(LoginRequiredMixin):
    model = ProgramLevel
    success_url = reverse_lazy('aadhyan:programlevel_list')
    form_class = ProgramLevelForm


class ProgramLevelList(ProgramLevelView, ListView):
    pass


class ProgramLevelCreate(ProgramLevelView, CreateView):
    pass


class ProgramLevelEdit(ProgramLevelView, UpdateView):
    pass


class ProgramLevelDelete(ProgramLevelView, DeleteView):
    pass


class CourseView(LoginRequiredMixin):
    model = Course
    success_url = reverse_lazy('aadhyan:course_list')
    form_class = CourseForm


class CourseList(CourseView, ListView):
    pass


class CourseCreate(CourseView, CreateView):
    pass


class CourseEdit(CourseView, UpdateView):
    pass


class CourseDelete(CourseView, DeleteView):
    pass


# TODO all methods should be processed according to active institute of institute admin
class InstituteUserView(LoginRequiredMixin):
    model = User
    success_url = reverse_lazy('aadhyan:instituteuser_list')
    form_class = InstituteUserForm


class InstituteUserList(InstituteUserView, ListView):
    pass


class InstituteUserCreate(InstituteUserView, CreateView):
    pass


class InstituteUserEdit(InstituteUserView, UpdateView):
    pass


class InstituteUserDelete(InstituteUserView, DeleteView):
    pass


class ChapterView(LoginRequiredMixin):
    model = ChapterPage
    success_url = reverse_lazy('aadhyan:chapter_list')
    form_class = ChapterForm

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        if course_id:
            return Course.objects.get(id=course_id).chapters.all()
        else:
            return []

    def get_context_data(self, **kwargs):
        context = super(ChapterView, self).get_context_data(**kwargs)
        context['course_id'] = self.kwargs.get('course_id')
        return context

    def get_success_url(self, **kwargs):
        course_id = self.kwargs.get('course_id')
        if course_id:
            return reverse_lazy('aadhyan:chapter_list', kwargs={'course_id': course_id})


class ChapterList(ChapterView, ListView):
    pass


class ChapterCreate(ChapterView, CreateView):
    def form_invalid(self, form):
        response = super(ChapterCreate, self).form_valid(form)
        self.object.course_id = self.kwargs.get('course_id')
        self.objet.save()
        return response


class ChapterEdit(ChapterView, UpdateView):
    def form_invalid(self, form):
        response = super(ChapterEdit, self).form_valid(form)
        self.object.course_id = self.kwargs.get('course_id')
        self.objet.save()
        return response


class ChapterDelete(ChapterView, DeleteView):
    pass


class TestView(LoginRequiredMixin):
    model = Test
    success_url = reverse_lazy('aadhyan:test_list')
    form_class = ChapterForm

    # def get_queryset(self):
    #     course_id = self.kwargs.get('course_id')
    #     if course_id:
    #         return Course.objects.get(id=course_id).chapters.all()
    #     else:
    #         return []

    # def get_context_data(self, **kwargs):
    #     context = super(ChapterView, self).get_context_data(**kwargs)
    #     context['course_id'] = self.kwargs.get('course_id')
    #     return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('aadhyan:test_list')


class TestListView(TestView, ListView):
    pass


class TestDeleteView(TestView, DeleteView):
    pass


class TestView(TemplateView, LoginRequiredMixin):
    template_name = 'academy/test.html'


class ChapterQuestion(TemplateView, LoginRequiredMixin):
    template_name = 'academy/chapterquestion_form.html'

    def get_context_data(self, **kwargs):
        context = super(ChapterQuestion, self).get_context_data(**kwargs)
        chapter_id = self.kwargs.get('chapter_id')

        queryset = ChapterPage.objects.get(id=chapter_id).questions.all()
        serializer = QuestionSerializer(queryset, many=True)
        context['initial_data'] = {'questions': serializer.data, 'chapter_id': chapter_id}
        context['forms'] = {
            'question_form': QuestionForm(),
            'choice_form': OptionForm()
        }

        return context

    def post(self, request, *args, **kwargs):
        chapter_id = self.kwargs.get('chapter_id')
        chapter = ChapterPage.objects.get(id=chapter_id)
        course_id = chapter.course.id
        params = json.loads(request.body.decode())
        # TODO move this logic to API
        with transaction.atomic():

            Question.objects.filter(id__in=params.get('questions_to_delete')).delete()

            for question in params.get('questions'):
                if question.get('id'):
                    question_obj = Question.objects.get(id=question.get('id'))
                else:
                    question_obj = Question()

                question_obj.detail = question.get('detail')

                if question.get('image').get('fileArray'):
                    question_obj.image.save(
                        question.get('image').get('file').get('name'),
                        base64_content_file(question.get('image').get('dataURL')),
                        save=False)
                question_obj.type = question.get('type')
                question_obj.true_false_answer = question.get('true_false_answer')
                question_obj.save()
                chapter.questions.add(question_obj)

                Option.objects.filter(id__in=question.get('choices_to_delete')).delete()

                for option in question.get('choices'):
                    if option.get('id'):
                        option_obj = Option.objects.get(id=option.get('id'))
                    else:
                        option_obj = Option()
                    option_obj.detail = option.get('detail')
                    option_obj.is_correct = option.get('is_correct')
                    option_obj.question = question_obj
                    option_obj.save()
        return JsonResponse({'success': True, 'course_id': course_id})


class TestCreateEditView(TemplateView, LoginRequiredMixin):
    template_name = 'academy/test_form.html'

    def get_context_data(self, **kwargs):
        context = super(TestCreateEditView, self).get_context_data(**kwargs)
        test_id = self.kwargs.get('test_id')

        if test_id:
            test = Test.objects.get(id=test_id)
            serializer = TestSerializer(test, many=False)
            context['initial_data'] = serializer.data
        else:
            context['initial_data'] = None

        context['forms'] = {
            'test_create_form': TestCreateForm(),
            'question_form': QuestionForm(),
            'choice_form': OptionForm()
        }

        return context

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode())
        test_id = self.kwargs.get('test_id', None)
        import ipdb
        ipdb.set_trace()
        with transaction.atomic():
            TestQuestion.objects.filter(id__in=data.get('test_questions_to_delete'))
            if data.get('id'):
                test = Test.objects.get(id=test_id)
            else:
                test = Test()

            test.name = data.get('name')
            test.course_id = data.get('course')
            test.pass_mark = data.get('pass_mark')
            test.created_by = request.user
            test.save()
            test_questions = []
            for chapter_question_data in data.get('chapter_questions'):
                chapter_question_id = chapter_question_data.get('id')
                if chapter_question_id:
                    chapter_question_obj = TestQuestion.objects.get(id=chapter_question_id)
                else:
                    chapter_question_obj = TestQuestion()
                chapter_question_obj.question_id = chapter_question_data.get('question')
                chapter_question_obj.chapter_id = chapter_question_data.get('chapter')
                chapter_question_obj.points = chapter_question_data.get('points')
                chapter_question_obj.save()
                test_questions.append(chapter_question_obj)

            for non_chapter_question_data in data.get('non_chapter_questions'):
                non_chapter_question_id = non_chapter_question_data.get('id')
                if non_chapter_question_id:
                    non_chapter_question_obj = TestQuestion.objects.get(id=non_chapter_question_id)
                else:
                    non_chapter_question_obj = TestQuestion()

                question_data = non_chapter_question_data.get('question')
                question_id = question_data.get('id')
                if question_id:
                    question_obj = Question.objects.get(id=question_id)
                else:
                    question_obj = Question()

                question_obj.detail = question_data.get('detail')

                if question_data.get('image').get('fileArray'):
                    question_obj.image.save(
                        question_data.get('image').get('file').get('name'),
                        base64_content_file(question_data.get('image').get('dataURL')),
                        save=False)
                question_obj.type = question_data.get('type')
                question_obj.true_false_answer = question_data.get('true_false_answer')
                question_obj.save()

                Option.objects.filter(id__in=question_data.get('choices_to_delete')).delete()

                for option_data in question_data.get('choices'):
                    if option_data.get('id'):
                        option_obj = Option.objects.get(id=option_data.get('id'))
                    else:
                        option_obj = Option()
                    option_obj.detail = option_data.get('detail')
                    option_obj.is_correct = option_data.get('is_correct')
                    option_obj.question = question_obj
                    option_obj.save()

                non_chapter_question_obj.question = question_obj
                non_chapter_question_obj.points = non_chapter_question_data.get('points')
                non_chapter_question_obj.save()

                test_questions.append(non_chapter_question_obj)

            test.questions.add(*test_questions)
        return JsonResponse({'success': True})


class QuizView(TemplateView, LoginRequiredMixin):
    template_name = 'academy/quiz.html'

    def get_context_data(self, **kwargs):
        context = super(QuizView, self).get_context_data(**kwargs)
        test_id = self.kwargs.get('test_id', None)
        chapter_id = self.kwargs.get('chapter_id', None)

        if test_id:
            test = Test.objects.get(id=test_id)
            test_question_serializer = TestQuestionDetailSerializer(test, many=True)
            context['test_questions'] = test_question_serializer.data
        elif chapter_id:
            chapter_questions = ChapterPage.objects.get(id=chapter_id).questions.all()
            chapter_question_serializer = QuestionSerializer(chapter_questions, many=True)
            context['chapter_questions'] = chapter_question_serializer.data
        else:
            context['test_questions'] = None
            context['chapter_questions'] = None
            context['student_id'] = self.request.user.id
            context['test_id'] = test_id
            context['chapter_id'] = chapter_id
        return context


class ChapterContentView(TemplateView, LoginRequiredMixin):
    template_name = 'academy/chaptercontent.html'

    def get_context_data(self, **kwargs):
        context = super(ChapterContentView, self).get_context_data(**kwargs)
        chapter_id = self.kwargs.get('chapter_id', None)
        if chapter_id:
            chapter_page_obj = ChapterPage.objects.get(id=chapter_id)
            context['object'] = chapter_page_obj
        else:
            context['object'] = None
        return context