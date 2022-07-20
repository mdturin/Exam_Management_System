from django.contrib.auth.views import LoginView, LogoutView, TemplateView
from django.urls import path

from dashboard.views import *

urlpatterns = [
    path('', dashboard, name='dashboard-page'),
    path('teacher-section', teacher_page, name='teacher-section'),
    path('staff-section', staff_page, name='staff-section'),
    path('routine-section', routine_page, name='routine-section'),
    path('full-routine', full_routine, name='full-routine'),
    path('add-exam', add_exam, name='add-exam'),
    path('add-staff', add_staff, name='add-staff'),
    path('add-teacher', add_teacher, name='add-teacher'),
]
