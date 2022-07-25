from account.models import *
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import redirect, render

from dashboard.models import *
from dashboard.routine_creator import *


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
        context['faculty'] = faculty
        context['staffs'] = get_staff(faculty)
        context['courses'] = get_courses(faculty_name)
        context['routines'] = get_routines(faculty)
        context['teachers'] = get_teachers(faculty_name)
        context['departments'] = list(
            Department.objects.filter(faculty=faculty))

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

    if request.method == 'POST':
        dept = request.POST.get('dept', '')
        level = request.POST.get('level', '')
        semester = request.POST.get('semester', '')
        type = request.POST.get('type', '')
        num_students = request.POST.get('num_students', '')
        start_date = request.POST.get('start_date', '')
        faculty = context['faculty']

        CreateRoutine(faculty, dept, level, semester,
                      type, num_students, start_date)

    LEVEL_CHOICES = ['1', '2', '3', '4']
    SEMESTER_CHOICES = ['I', 'II']
    EXAM_TYPES = ['Theory', 'LAB']

    context['levels'] = LEVEL_CHOICES
    context['semesters'] = SEMESTER_CHOICES
    context['types'] = EXAM_TYPES

    return render(request, 'add-exam.html', context)


def add_staff(request):

    context = get_context(request)

    if request.method == 'POST':
        fname = request.POST.get('first_name', '')
        lname = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        mobile = request.POST.get('mobile', '')
        picture = request.POST.get('picture')
        faculty = context['faculty']

        try:
            with transaction.atomic():
                user = User(
                    username=email,
                    email=email,
                    first_name=fname,
                    last_name=lname,
                )

                user.save()

                staff = Staff.objects.create(
                    user=user,
                    contact_number=mobile,
                    faculty=faculty,
                )

                staff.profile_picture = get_directory(user.id, picture)
                staff.save()

        except:
            return redirect('add-staff')

        return redirect('staff-section')

    return render(request, 'add-staff.html', context)


def get_directory(user_id, filename: str):
    return f'img/pp/{user_id}_{filename}'


def add_teacher(request):

    if request.method == 'POST':
        fname = request.POST.get('first_name', '')
        lname = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        title = request.POST.get('title', '')
        mobile = request.POST.get('mobile', '')
        picture = request.POST.get('picture')
        dept = request.POST.get('dept', '')

        try:
            with transaction.atomic():
                user = User(
                    username=email,
                    email=email,
                    first_name=fname,
                    last_name=lname,
                )

                user.save()

                teacher = Teacher.objects.create(
                    user=user,
                    title=title,
                    contact_number=mobile,
                    department=Department.objects.get(name=dept)
                )

                teacher.profile_picture = get_directory(user.id, picture)
                teacher.save()

        except:
            return redirect('add-teacher')

        return redirect('teacher-section')

    TEACHER_TITLE_CHOICES = [
        'Professor', 'Associate Professor', 'Assistant Professor', 'Lecturer', 'None']

    context = get_context(request)
    context['titles'] = TEACHER_TITLE_CHOICES

    return render(request, 'add-teacher.html', context)


def edit_teacher(request):
    context = get_context(request)
    return render(request, 'edit-teacher.html', context)


def edit_staff(request):
    context = get_context(request)
    return render(request, 'edit-staff.html', context)
