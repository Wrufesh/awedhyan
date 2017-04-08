from django.conf import settings
from django.db import models
from django.db.models.signals import pre_delete
from django.utils.translation import ugettext as _
from redactor.fields import RedactorField

from app.apps.academy.signal_receivers import delete_question_choice, delete_non_chapter_question, delete_test_question


class Institute(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class BoardOrUniversity(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = _('Board or Universities')

    def __str__(self):
        return self.name


class Faculty(models.Model):
    name = models.CharField(max_length=150)
    board_or_university = models.ForeignKey(
        BoardOrUniversity,
        related_name='faculties'
    )

    class Meta:
        verbose_name_plural = _('Faculties')

    def __str__(self):
        return '%s[%s]' % (self.name, self.board_or_university)


class ProgramLevel(models.Model):
    name = models.CharField(max_length=150)
    program = models.ForeignKey(
        Faculty,
        related_name='faculty_program_levels'
    )

    def __str__(self):
        return '%s[%s]' % (self.name, self.program)


class Program(models.Model):
    name = models.CharField(max_length=150)
    faculty = models.ForeignKey(
        ProgramLevel,
        related_name='program_level_programs'
    )

    def __str__(self):
        return '%s[%s]' % (self.name, self.faculty)


# End of can only be added by superuser


class Course(models.Model):
    name = models.CharField(max_length=100)
    program = models.ForeignKey(
        Program,
        related_name='education_program_courses',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    contributed_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='instructor_courses')
    institute = models.ForeignKey(
        Institute,
        related_name='institute_courses',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return '%s-%s-%s' % (self.name, self.program, self.institute)


class Question(models.Model):
    type_choices = (
        ('OBJECTIVE', _('Objective')),
        ('TRUE/FALSE', _('True/False')),
        ('ESSAY', _('Essay')),
    )
    detail = models.CharField(max_length=1000)

    image = models.ImageField(upload_to='question/', height_field=None, width_field=None, null=True, blank=True)

    type = models.CharField(max_length=256, choices=type_choices)

    # The below field is present when the question type is True/False Type
    true_false_answer = models.BooleanField(default=False)

pre_delete.connect(delete_question_choice, sender=Question)


# class EssayAnswer(models.Model):
#     question = models.ForeignKey(Question, related_name='essay_answers')
#     student = models.ForeignKey(settings.AUTH_USER_MODEL)
#     answer_image = models.ImageField(upload_to='essay_answer/', height_field=None, width_field=None, max_length=100)
#
#     essay_answer_status_choices = (
#         ('CHECKED', _('Checked')),
#         ('UNCHECKED', _('Unchecked')),
#     )
#     status = models.CharField(max_length=128, choices=essay_answer_status_choices)
#     marks_obtained = models.PositiveIntegerField(null=True, blank=True)


class ChapterPage(models.Model):
    name = models.CharField(max_length=128)
    course = models.ForeignKey(Course, related_name="chapters")

    content = RedactorField()

    questions = models.ManyToManyField(Question,blank=True)

    def __str__(self):
        return '%s-%s' % (self.name, self.course)


class Test(models.Model):
    name = models.CharField(max_length=250)
    course = models.ForeignKey(Course)
    pass_mark = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tests')

    def get_chapter_questions(self):
        return self.questions.all().filter(chapter__isnull=False)

    def get_non_chapter_questions(self):
        return self.questions.all().filter(chapter__isnull=True)

    def __str__(self):
        return self.name

pre_delete.connect(delete_test_question, sender=Test)


class TestQuestion(models.Model):
    test = models.ForeignKey(Test, related_name='questions')
    chapter = models.ForeignKey(ChapterPage, null=True, blank=True)
    question = models.ForeignKey(Question, related_name='tests')
    points = models.PositiveIntegerField()

pre_delete.connect(delete_non_chapter_question, sender=TestQuestion)


class Option(models.Model):
    detail = models.CharField(max_length=1000)
    question = models.ForeignKey(Question, related_name="choices")
    is_correct = models.BooleanField(default=False)


class TestQuestionAnswer(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='test_question_answers')
    # test = models.ForeignKey(Test, related_name='test_question_answers')
    test_question = models.ForeignKey(TestQuestion, related_name='test_question_answers')
    true_false_answer = models.BooleanField(default=False)
    option_answers = models.ManyToManyField(Option)
    # below two activates when question type is of essay
    essay_answer_content = RedactorField(blank=True, null=True)
    points = models.PositiveIntegerField()

    class Meta:
        unique_together= ('student', 'test_question')

    @classmethod
    def get_auto_computable_marks(cls, test_obj, student):
        auto_computable_question_types = ['TRUE/FALSE', 'OBJECTIVE']
        pass

    @classmethod
    def get_non_auto_computable_marks(cls, test_obj, student):
        non_auto_computable_types = ['ESSAY']
        pass

