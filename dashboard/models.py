from django.db import models

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


class Faculty(models.Model):
    name = models.CharField(max_length=255, null=False)

    def __str__(self) -> str:
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=255, null=True)

    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.name


class Course(models.Model):

    code = models.CharField(max_length=255, null=False)

    credits = models.FloatField(null=False)

    department = models.OneToOneField(
        Department, on_delete=models.CASCADE, null=False)

    is_sessional = models.BooleanField(null=False, default=False)

    level = models.CharField(max_length=1, null=False,
                             choices=LEVEL_CHOICES, default='1')

    name = models.CharField(max_length=255, null=False)

    semester = models.CharField(
        max_length=2, null=False, choices=SEMESTER_CHOICES, default='I')

    def __str__(self) -> str:
        return f"{ self.code }"
