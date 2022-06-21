from django.db import models
from django.contrib.auth.models import User

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

TEACHER_TITLE_CHOICES = [
    ('Professor', 'Professor'),
    ('Associate Professor', 'Associate Professor'),
    ('Assistant Professor', 'Assistant Professor'),
    ('Lecturer', 'Lecturer'),
    ('None', 'None'),
]


def get_profile_pictures_directory(self: 'Teacher', filename: str):
    return f'img/pp/{self.user.id}_{filename}'


class Teacher(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=255, null=False,
                             choices=TEACHER_TITLE_CHOICES, default='None')

    contact_number = models.CharField(null=False, unique=True, max_length=11)

    profile_picture = models.ImageField(
        upload_to=get_profile_pictures_directory, blank=True, null=True)

    is_dean = models.BooleanField(default=False, null=False)

    def __str__(self) -> str:
        return self.user.email

    @property
    def get_instance(self):
        return self

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name
