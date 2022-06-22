from django.shortcuts import render

from account.forms import *
from account.models import *


def register_page(request):
    return render(request, 'register_page.html', {'title': 'Sign Up'})
