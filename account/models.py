from django.db import models

from account.choices import *
from account.validator import contact_number_validator


def get_profile_pictures_directory(self: 'Member', filename: str):
    return f'img/pp/{self.username}'


class Member(models.Model):

    first_name = models.CharField(max_length=255, null=False)

    last_name = models.CharField(max_length=255, null=False)

    password = models.CharField(max_length=31, null=False)

    email = models.EmailField(max_length=255, null=False, unique=True)

    title = models.CharField(max_length=255, null=False,
                             choices=TEACHER_TITLE_CHOICES, default='None')

    contact_number = models.CharField(
        null=False, unique=True, max_length=11,
        validators=[contact_number_validator],
    )

    profile_picture = models.ImageField(
        upload_to=get_profile_pictures_directory, null=False, blank=False)

    is_dean = models.BooleanField(default=False, null=False)

    is_teacher = models.BooleanField(default=False, null=False)

    is_staff = models.BooleanField(default=False, null=False)

    def __str__(self) -> str:
        return self.email


class Faculty(models.Model):
    name = models.CharField(max_length=255, null=False)

    short_name = models.CharField(max_length=255, null=False)

    def __str__(self) -> str:
        return self.name + f" ({self.short_name})"


class Department(models.Model):
    name = models.CharField(max_length=255, null=False)

    short_name = models.CharField(max_length=255, null=False)

    facutly = models.OneToOneField(
        Faculty, on_delete=models.PROTECT, null=False)

    def __str__(self) -> str:
        return self.name + f" ({self.short_name})"


class Course(models.Model):

    name = models.CharField(max_length=255, null=False)

    credits = models.FloatField(null=False)

    code = models.CharField(max_length=255, null=False)

    level = models.CharField(max_length=1, null=False,
                             choices=LEVEL_CHOICES, default='1')

    semester = models.CharField(
        max_length=2, null=False, choices=SEMESTER_CHOICES, default='I')

    is_sessional = models.BooleanField(null=False, default=False)

    department = models.OneToOneField(
        Department, on_delete=models.CASCADE, null=False)

    def __str__(self) -> str:
        return self.name + f" ({self.code})"
