from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from account.views import *

urlpatterns = [
    path('', LoginView.as_view(template_name='login_page.html'), name='login-page'),
    path('register/', register_page, name='register-page'),
    path('logout/', LogoutView.as_view(template_name='logout_page.html'),
         name='logout-page'),
]
