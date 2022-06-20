from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login

from account.forms import *
from account.models import *


def register_page(request):
    return render(request, 'register_page.html')


def login_page(request):
    userForm = LoginForm()
    if request.method == 'POST':
        userForm = LoginForm(request.POST)
        if userForm.is_valid():
            email = userForm.cleaned_data['email']
            password = userForm.cleaned_data['password']
            remember_me = userForm.cleaned_data['remember_me']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                return redirect('dashboard-page')
        else:
            print("Member Form isn't valid")
    return render(request, 'login_page.html', {'form': userForm})
