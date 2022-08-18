from datetime import date

from account.models import *
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import redirect, render
from django.views.generic.edit import DeleteView

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
    return list(Exam.objects.filter(faculty=faculty))


def get_teachers(faculty):
    teachers = Teacher.objects.all()

    selected_teachers = []
    for teacher in teachers:
        dept = Department.objects.get(name=teacher.department)
        if dept.faculty == faculty:
            selected_teachers.append(teacher)

    return selected_teachers


def get_exams(approved_routines, teacher=None):
    past = []
    current = []
    upcomming = []

    today = date.today()
    for routine in approved_routines:
        exams = routine.exam_set.all()
        if teacher:
            exams = filter(lambda exam: teacher in exam.examiners.all()
                           or teacher == exam.supervisor, exams)
        for exam in exams:
            if exam.exam_date == today:
                current.append(exam)
            elif exam.exam_date < today:
                past.append(exam)
            else:
                upcomming.append(exam)

    return current, past, upcomming


def get_context(request, full_routine=False):
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
        'if_staff': staff is not None,
        'if_dean': dean is not None,
        'user': staff or teacher,
    }
    
    if context['is_staff'] or full_routine:
        approved_routines = Routine.objects.filter(is_approved=True).all()
        current, past, upcomming = get_exams(approved_routines)
        context['current_exams'] = current
        context['past_exams'] = past
        context['upcomming_exams'] = upcomming
        routines = Routine.objects.filter(is_approved=False).all()
        context['routines'] = routines

    if context['is_staff']:
        faculty = Faculty.objects.get(name=faculty_name)
        context['faculty'] = faculty
        context['staffs'] = get_staff(faculty)
        context['courses'] = get_courses(faculty_name)
        context['teachers'] = get_teachers(faculty_name)
        context['departments'] = list(
            Department.objects.filter(faculty=faculty))
        year = date.today().year
        context['year'] = year
        context['events'] = Event.objects.filter(
            start_date__year=year).all()

    elif not full_routine:
        approved_routines = Routine.objects.filter(is_approved=True).all()
        current, past, upcomming = get_exams(approved_routines, teacher)
        context['current_exams'] = current
        context['past_exams'] = past
        context['upcomming_exams'] = upcomming

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


def course_page(request):
    context = get_context(request)
    return render(request, 'course-section.html', context)


def routine_page(request):
    context = get_context(request)
    return render(request, 'routine-section.html', context)


def event_page(request):
    context = get_context(request)
    return render(request, 'event-section.html', context)


def profile_page(request):
    context = get_context(request)
    return render(request, 'profile-section.html', context)


def full_routine(request):
    context = get_context(request, True)
    return render(request, 'full-routine.html', context)


def add_routine(request):
    context = get_context(request)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        dept = request.POST.get('dept', '')
        level = request.POST.get('level', '')
        semester = request.POST.get('semester', '')
        type = request.POST.get('type', '')
        num_students = request.POST.get('num_students', '')
        start_date = request.POST.get('start_date', '')
        faculty = context['faculty']

        CreateRoutine(name, faculty, dept, level, semester,
                      type == 'LAB', int(num_students), start_date)

        return redirect('routine-section')

    LEVEL_CHOICES = ['1', '2', '3', '4']
    SEMESTER_CHOICES = ['I', 'II']
    EXAM_TYPES = ['Theory', 'LAB']

    context['levels'] = LEVEL_CHOICES
    context['semesters'] = SEMESTER_CHOICES
    context['types'] = EXAM_TYPES

    return render(request, 'add-routine.html', context)


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


class TeacherDeleteView(DeleteView):
    model = Teacher
    success_url = '/'
    template_name = 'teacher_confirm_delete.html'


class StaffDeleteView(DeleteView):
    model = Staff
    success_url = '/'
    template_name = 'staff_confirm_delete.html'


class EventDeleteView(DeleteView):
    model = Event
    success_url = '/'
    template_name = 'event_confirm_delete.html'

class CourseDeleteView(DeleteView):
    model = Course
    success_url = '/'
    template_name = 'course_confirm_delete.html'

def add_event(request):
    context = get_context(request)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        notes = request.POST.get('notes', '')
        event = Event.objects.create(
            name=name,
            start_date=start_date,
            end_date=end_date,
            notes=notes,
        )
        event.save()
        return render(request, 'event-section.html', context)
    return render(request, 'add-event.html', context)


def edit_event(request):
    context = get_context(request)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        notes = request.POST.get('notes', '')
        event = Event.objects.create(
            name=name,
            start_date=start_date,
            end_date=end_date,
            notes=notes,
        )
        event.save()
        return render(request, 'event-section.html', context)
    return render(request, 'add-event.html', context)

def add_course(request):
    context = get_context(request)

    if request.method == 'POST':
        level = request.POST.get('level', '')
        semester = request.POST.get('semester', '')
        code = request.POST.get('code', '')
        course_title = request.POST.get('name', '')
        credit = request.POST.get('credits', '')
        course_type = request.POST.get('is_sessional', '')
        course = Course.objects.create(
            level=level,
            semester=semester,
            code=code,
            name=course_title,
            credits=credit,
            is_sessional=course_type,
        )
        course.save()
        return render(request, 'course-section.html', context)
    return render(request, 'add-course.html', context)


def edit_course(request):
    context = get_context(request)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        notes = request.POST.get('notes', '')
        event = Event.objects.create(
            name=name,
            start_date=start_date,
            end_date=end_date,
            notes=notes,
        )
        event.save()
        return render(request, 'course-section.html', context)
    return render(request, 'edit-course.html', context)


# @login_required(login_url='deanlogin')
def dean_view_pending_routine(request):
    context = get_context(request)
    return render(request,'dean_view_pending_routine.html', context)

# @login_required(login_url='adminlogin')
def approve_routine_view(request,pk):
    context = get_context(request)
    routine= Routine.objects.get(id=pk)
    routine.is_approved=True
    
    routine.save()
    return render(request,'dean_view_pending_routine.html', context)

# @login_required(login_url='adminlogin')
def reject_routine_view(request,pk):
    context = get_context(request)
    routine= Routine.objects.get(id=pk)
    routine.delete()
    return render(request,'dean_view_pending_routine.html', context)

