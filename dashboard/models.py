from django.db import models

# Create your models here.


# class Faculty(models.Model):
#     name = models.CharField(max_length=255, null=False)

#     short_name = models.CharField(max_length=255, null=False)

#     def __str__(self) -> str:
#         return self.name + f" ({self.short_name})"


# class Department(models.Model):
#     name = models.CharField(max_length=255, null=False)

#     short_name = models.CharField(max_length=255, null=False)

#     facutly = models.OneToOneField(
#         Faculty, on_delete=models.PROTECT, null=False)

#     def __str__(self) -> str:
#         return self.name + f" ({self.short_name})"


# class Course(models.Model):

#     name = models.CharField(max_length=255, null=False)

#     credits = models.FloatField(null=False)

#     code = models.CharField(max_length=255, null=False)

#     level = models.CharField(max_length=1, null=False,
#                              choices=LEVEL_CHOICES, default='1')

#     semester = models.CharField(
#         max_length=2, null=False, choices=SEMESTER_CHOICES, default='I')

#     is_sessional = models.BooleanField(null=False, default=False)

#     department = models.OneToOneField(
#         Department, on_delete=models.CASCADE, null=False)

#     def __str__(self) -> str:
#         return self.name + f" ({self.code})"
