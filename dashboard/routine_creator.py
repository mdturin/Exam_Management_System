from zoneinfo import available_timezones
from account.models import *
from dashboard.models import *

available_teachers = Teacher.objects.filter(is_available=True)


def get_teachers(faculty_name):
    faculty = Faculty.objects.get(name=faculty_name)
    departments = faculty.department_set.all()
    teachers = available_teachers.filter(department__in=departments)

    examiners = []
    supervisors = []

    for teacher in teachers:
        if teacher.check_supervisor:
            supervisors.append(teacher)
        else:
            examiners.append(teacher)

    return supervisors, examiners


def CreateRoutine(
        faculty_name, department_name, level, semester, exam_type, num_students, start_date):
    supervisors, examiners = get_teachers(faculty_name)
    department = Department.objects.get(name=department_name)
    courses = department.course_set.filter(
        level=level, semester=semester, is_sessional=exam_type)
