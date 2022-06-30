from django.test import TestCase

import random
from account.models import *

faculies = list(Faculty.objects.all())
sz = len(faculies)

names = ["ECE", "CSE", "EEE", "ME", "CE", "Agri"]
for name in names:
    dept = Department()
    dept.name = name
    p = random.randint(0, sz-1)
    dept.faculty = faculies[p]
    dept.save()
