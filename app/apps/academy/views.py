import json

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from .serializers import QuestionSerializer
from app.utils.mixins import DeleteView, UpdateView, CreateView, LoginRequiredMixin
from .forms import BoardForm, FacultyForm, ProgramForm, ProgramLevelForm, InstituteForm, CourseForm, ChapterForm, \
    QuestionForm, OptionForm
from .models import BoardOrUniversity, Faculty, Program, ProgramLevel, Institute, Course, ChapterPage, Question, Option

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
    pass


class ChapterEdit(ChapterView, UpdateView):
    pass


class ChapterDelete(ChapterView, DeleteView):
    pass


def base64_content_file(data):
    import base64
    from django.core.files.base import ContentFile
    format, imgstr = data.split(';base64,')
    ext = format.split('/')[-1]

    data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    return data


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
        # import ipdb
        # ipdb.set_trace()
        params = json.loads(request.body.decode())

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
        return JsonResponse({'success': True})




