from django import forms
from app.apps.academy.models import BoardOrUniversity, Faculty, Program, ProgramLevel, Course, Institute, ChapterPage
from app.utils.forms import HTML5BootstrapModelForm


class InstituteForm(HTML5BootstrapModelForm):
    class Meta:
        model = Institute
        fields = '__all__'


class BoardForm(HTML5BootstrapModelForm):
    class Meta:
        model = BoardOrUniversity
        fields = '__all__'


class FacultyForm(HTML5BootstrapModelForm):
    class Meta:
        model = Faculty
        fields = '__all__'
        widgets = {
            'board_or_university': forms.Select(attrs={'class': 'selectize'}, ),
        }


class ProgramForm(HTML5BootstrapModelForm):
    class Meta:
        model = Program
        fields = '__all__'
        widgets = {
            'faculty': forms.Select(attrs={'class': 'selectize'}, ),
        }


class ProgramLevelForm(HTML5BootstrapModelForm):
    class Meta:
        model = ProgramLevel
        fields = '__all__'
        widgets = {
            'program': forms.Select(attrs={'class': 'selectize'}, ),
        }


class CourseForm(HTML5BootstrapModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'level': forms.Select(attrs={'class': 'selectize'}, ),
            'institute': forms.Select(attrs={'class': 'selectize'}, ),
            'contributed_by': forms.SelectMultiple(attrs={'class': 'selectize'}, ),
        }


class ChapterForm(HTML5BootstrapModelForm):

    class Meta:
        model = ChapterPage
        fields = '__all__'
