from django.contrib.auth.models import User
from django.db import models

from app_test.validator import contact_number_validator


def get_profile_pictures_directory(self: 'TestMember', filename):
    return f'img/pp/{self.username}'


class TestMember(User):

    # username

    # first_name

    # last_name

    # email

    # password

    # is_staff

    organization = models.CharField(max_length=255, null=False)

    contact_number = models.CharField(
        max_length=11,
        null=False,
        validators=[contact_number_validator]
    )

    profile_picture = models.ImageField(
        upload_to=get_profile_pictures_directory, null=False, blank=False)

    is_dean = models.BooleanField(default=False, null=False)

    is_teacher = models.BooleanField(default=False, null=False)


class TestDepartment(models.Model):
    name = models.CharField(max_length=255, null=False)


class TestCourse(models.Model):

    LEVEL_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ]

    SEMESTER_CHOICES = [
        ('I', 'I'),
        ('II', 'II'),
    ]

    name = models.CharField(max_length=255, null=False)

    credits = models.FloatField(null=False)

    code = models.CharField(max_length=255, null=False)

    level = models.CharField(max_length=1, null=False,
                             choices=LEVEL_CHOICES, default='1')

    semester = models.CharField(
        max_length=2, null=False, choices=SEMESTER_CHOICES, default='I')

    department = models.OneToOneField(
        TestDepartment, on_delete=models.CASCADE, null=False)
