from django.contrib.auth.views import LoginView, LogoutView, TemplateView

from django.urls import path

from dashboard.views import *

urlpatterns = [
    path('', dashboard, name='dashboard-page'),
    path('teacher-section', teacher_page, name='teacher-section'),
    path('staff-section', staff_page, name='staff-section'),
    path('profile-section', profile_page, name='profile-section'),
    path('course-section', course_page, name='course-section'),
    path('routine-section', routine_page, name='routine-section'),
    path('event-section', event_page, name='event-section'),
    path('full-routine', full_routine, name='full-routine'),
    path('add-routine', add_routine, name='add-routine'),
    path('add-staff', add_staff, name='add-staff'),
    path('add-teacher', add_teacher, name='add-teacher'),
    path('add-event', add_event, name='add-event'),
    path('add-course', add_course, name='add-course'),
    path('edit-teacher', edit_teacher, name='edit-teacher'),
    path('edit-staff', edit_staff, name='edit-staff'),
    path('edit-event', edit_event, name='edit-event'),
    path('edit-course', edit_course, name='edit-course'),
    path('delete-teacher/<pk>', TeacherDeleteView.as_view(), name='delete-teacher'),
    path('delete-staff/<pk>', StaffDeleteView.as_view(), name='delete-staff'),
    path('delete-event/<pk>', EventDeleteView.as_view(), name='delete-event'),
    path('delete-course/<pk>', CourseDeleteView.as_view(), name='delete-course'),
]
