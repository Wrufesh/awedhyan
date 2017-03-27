from django import forms
from app.apps.academy.models import BoardOrUniversity, Faculty, Program, ProgramLevel, Course, Institute, ChapterPage, \
    Option, Question
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


class OptionForm(HTML5BootstrapModelForm):
    class Meta:
        model = Option
        fields = ('detail', 'is_correct')

        widgets = {
            'detail': forms.TextInput(attrs={'data-bind': 'value: detail'}),
            'is_correct': forms.CheckboxInput(attrs={'data-bind': 'checked: detail'})
        }


class QuestionForm(HTML5BootstrapModelForm):
    class Meta:
        # 'detail', 'image', 'true_false_answer', 'type', 'choices'
        model = Question
        fields = ('detail', 'image', 'true_false_answer', 'type')

        widgets = {
            'detail': forms.TextInput(attrs={'data-bind': 'value: detail'}),
            'image': forms.ClearableFileInput(attrs={'data-bind': 'value: image'}),
            'true_false_answer': forms.CheckboxInput(attrs={'data-bind' : 'checked: true_false_answer'}),
            'type': forms.Select(attrs={'data-bind': 'value: type'})
        }