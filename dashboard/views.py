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


def is_teacher(user):
    try:
        teacher = Teacher.objects.get(user=user)
    except Teacher.DoesNotExist:
        return None
    return teacher


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


def get_context(request):
    faculty_name = None
    dean = is_dean(request.user)
    staff = is_staff(request.user)
    teacher = is_teacher(request.user)

    if staff:
        faculty_name = staff.faculty
    elif dean:
        faculty_name = dean.faculty

    context = {
        'is_staff': (staff != None or dean != None),
        'if_staff': staff, 
        'if_dean': dean,
        'user': staff or teacher
    }

    if context['is_staff']:
        faculty = Faculty.objects.get(name=faculty_name)
        context['staffs'] = get_staff(faculty)
        context['courses'] = get_courses(faculty_name)
        context['routines'] = get_routines(faculty)
        context['teachers'] = get_teachers(faculty_name)
        context['departments'] = list(Department.objects.filter(faculty=faculty))

    return context


def dashboard(request):
    context = get_context(request)
    return render(request, 'dashboard.html', context)


def teacher_page(request):
    context = get_context(request)
    return render(request, 'teacher-section.html', context)


def staff_page(request):
    context = get_context(request)
    return render(request, 'staff-section.html', context)


def routine_page(request):
    context = get_context(request)
    return render(request, 'routine-section.html', context)

def full_routine(request):
    context = get_context(request)
    return render(request, 'full-routine.html', context)

def add_exam(request):
    context = get_context(request)
    return render(request, 'add-exam.html', context)

def add_staff(request):
    context = get_context(request)
    return render(request, 'add-staff.html', context)

def add_teacher(request):
    context = get_context(request)
    return render(request, 'add-teacher.html', context)