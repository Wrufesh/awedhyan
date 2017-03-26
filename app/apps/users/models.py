from django.contrib.auth.models import AbstractUser
from app.apps.academy.models import Institute
from django.db import models


class User(AbstractUser):
    institute = models.ForeignKey(Institute, on_delete=models.SET_NULL, blank=True, null=True)
    # pass
