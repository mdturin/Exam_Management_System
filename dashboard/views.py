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


def has_permission(user):
    return is_staff(user) != None or is_dean(user) != None


def dashboard(request):
    context = {
        'title': 'Dashboard',
        'is_staff': has_permission(request.user),
    }

    faculty = None
    staff = is_staff(request.user)
    dean = is_dean(request.user)

    if staff:
        faculty = staff.faculty
    else:
        faculty = dean.faculty

    if context['is_staff']:
        context['staffs'] = Staff.objects.filter(faculty=faculty)
        context['courses'] = Course.objects.all()
        context['routines'] = Routine.objects.all()
        context['teachers'] = Teacher.objects.all()

    return render(request, 'dashboard.html', context)
