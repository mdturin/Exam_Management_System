import datetime

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


def get_date(date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()


def get_next_date(cur_date):
    return cur_date + datetime.timedelta(days=1)


def get_next_events(cur_date):
    return Event.objects.filter(start_date__lte=cur_date, end_date__gte=cur_date).all()


def get_available_date(cur_date):

    if cur_date.weekday() == 4:
        cur_date = get_next_date(cur_date)

    if cur_date.weekday() == 5:
        cur_date = get_next_date(cur_date)

    events = get_next_events(cur_date)
    if len(events) == 0:
        return cur_date

    cur_date = events[0].end_date
    cur_date = get_next_date(cur_date)
    return get_available_date(cur_date)


def CreateRoutine(
        faculty_name, department_name, level, semester, exam_type, num_students, date_str):

    supervisors, examiners = get_teachers(faculty_name)
    department = Department.objects.get(name=department_name)

    courses = department.course_set.filter(
        level=level, semester=semester, is_sessional=exam_type)

    routine = Routine()
    routine.is_approved = False

    cur_date = get_date(date_str)

    
