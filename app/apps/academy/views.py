from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import ListView

from .serializers import QuestionSerializer
from app.utils.mixins import DeleteView, UpdateView, CreateView, LoginRequiredMixin
from .forms import BoardForm, FacultyForm, ProgramForm, ProgramLevelForm, InstituteForm, CourseForm, ChapterForm
from .models import BoardOrUniversity, Faculty, Program, ProgramLevel, Institute, Course, ChapterPage

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


class ChapterQuestion(TemplateView):
    template_name = 'aadhyan/chapterquestion_form.html'

    def get_context_data(self, **kwargs):
        context = super(ChapterQuestion, self).get_context_data(**kwargs)
        chapter_id = self.kwargs.get('chapter_id')

        queryset = ChapterPage.objects.get(id=chapter_id).questions.all()
        serializer = QuestionSerializer(queryset, many=True)
        context['initial_data'] = serializer.data
        context['chapter_id'] = chapter_id
        return context