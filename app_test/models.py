from django.db import models
from django.contrib.auth.models import User

class TestMember(User):
    organization = models.CharField(max_length=255, null=False)
    