from django.contrib.auth.models import AbstractUser
from app.apps.academy.models import Institute, ProgramLevel
from django.db import models


class User(AbstractUser):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, blank=True, null=True)
    # follow field only populates when user is student
    program_level = models.ForeignKey(ProgramLevel, on_delete=models.CASCADE, blank=True, null=True)
    # pass

    @property
    def groups_name(self):
        return [obj.name for obj in self.groups.all()]