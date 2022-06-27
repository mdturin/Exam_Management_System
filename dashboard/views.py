from asyncio import selector_events
from django.shortcuts import render
from account.models import *
from dashboard.models import *


def is_dean(user):
    try:
        teacher = Teacher.objects.get(user=user)
    except Teacher.DoesNotExist:
        return None

    deans = Dean.objects.filter(teacher=teacher).order_by('-joined')[:1]
    if len(deans) != 1:
        return None

    return deans[0]


def is_staff(user):
    try:
        staff = Staff.objects.get(user=user)
    except Staff.DoesNotExist:
        return None
    return staff


def get_staff(faculty):
    return list(Staff.objects.filter(faculty=faculty))


def get_courses(faculty):
    courses = Course.objects.all()

    selected_courses = []
    for course in courses:
        dept = Department.objects.get(name=course.department)
        if dept.faculty == faculty:
            selected_courses.append(course)

    return selected_courses


def get_routines(faculty):
    return list(Routine.objects.filter(faculty=faculty))


def get_teachers(faculty):
    teachers = Teacher.objects.all()

    selected_teachers = []
    for teacher in teachers:
        dept = Department.objects.get(name=teacher.department)
        if dept.faculty == faculty:
            selected_teachers.append(teacher)

    return selected_teachers


def dashboard(request):
    faculty_name = None
    dean = is_dean(request.user)
    staff = is_staff(request.user)

    if staff:
        faculty_name = staff.faculty
    elif dean:
        faculty_name = dean.faculty

    context = {
        'is_staff': (staff != None or dean != None)
    }

    if context['is_staff']:
        faculty = Faculty.objects.get(name=faculty_name)
        context['staffs'] = get_staff(faculty)
        context['courses'] = get_courses(faculty_name)
        context['routines'] = get_routines(faculty)
        context['teachers'] = get_teachers(faculty_name)

        print(faculty_name)
        print(context['routines'])

    return render(request, 'dashboard.html', context)
