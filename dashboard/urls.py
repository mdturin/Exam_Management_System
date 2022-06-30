from django.contrib.auth.views import LoginView, LogoutView, TemplateView
from django.urls import path

from dashboard.views import *

urlpatterns = [
    path('', dashboard, name='dashboard-page'),
    path('teacher-section', teacher_page, name='teacher-section'),
    path('staff-section', TemplateView.as_view(template_name="staff-section.html"),
         name='staff-section'),
    path('routine-section', TemplateView.as_view(template_name="routine-section.html"),
         name='routine-section'),
]
