from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from app.apps.academy.models import Institute, ProgramLevel
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
            date_of_birth=date_of_birth
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, blank=True, null=True)
    # follow field only populates when user is student
    program_level = models.ForeignKey(ProgramLevel, on_delete=models.CASCADE, blank=True, null=True)
    # pass

    @property
    def groups_name(self):
        return [obj.name for obj in self.groups.all()]