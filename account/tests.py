from django.test import TestCase
from faker import Faker

import random
from account.models import *

fake = Faker()

faculies = list(Faculty.objects.all())
sz_f = len(faculies)

depts = list(Department.objects.all())
sz_d = len(depts)

for dept in depts:
    for x in range(101, 104):
        course = Course()
        course.code = dept.name + str(x)
        x = random.choices([0.75, 1.5, 2, 3], k=1)[0]
        course.credits = x
        course.department = depts[random.randint(0, sz_d-1)]
        if x < 2:
            course.is_sessional = True if random.randint(0, 10) >= 5 else False
        course.level = random.randint(1, 5)
        course.semester = ['I', 'II'][random.randint(0, 1)]
        course.name = fake.job()
        course.save()
