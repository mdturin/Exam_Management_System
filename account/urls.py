from django.urls import path
from account.views import *


urlpatterns = [
    path('', login_page, name='login-page'),
]
