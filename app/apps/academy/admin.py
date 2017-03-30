from django.contrib import admin
from .models import Institute, BoardOrUniversity, Faculty, Program, ProgramLevel, Course, Question, Option

admin.site.register(Institute)
admin.site.register(BoardOrUniversity)
admin.site.register(Faculty)
admin.site.register(Program)
admin.site.register(ProgramLevel)
admin.site.register(Course)
admin.site.register(Question)
admin.site.register(Option)