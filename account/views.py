from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login

from account.forms import *
from account.models import *


# def dashboard(request):
#     return render(request, 'dashboard.html')


# def register_page(request):
#     formErrors = {}
#     userForm = UserRegistraionForm()
#     memberForm = MemberRegisterForm()

#     context = {
#         'user': userForm,
#         'member': memberForm,
#         'errors': formErrors,
#     }

#     if request.method == 'POST':
#         userForm = UserRegistraionForm(request.POST)
#         memberForm = MemberRegisterForm(request.POST, request.FILES)
#         if userForm.is_valid() and memberForm.is_valid():
#             user = userForm.save(commit=False)
#             user.set_password(userForm.cleaned_data['password'])
#             user.username = user.email
#             user.save()

#             member = memberForm.save(commit=False)
#             member.user = user
#             member.save()

#             return redirect('login-page')
#         else:
#             print("Member Form isn't valid")
#             formErrors = memberForm.errors.as_json()
#             print(formErrors)

#     return render(request, 'register_page.html', context)


# def login_page(request):
#     memberForm = LoginForm()
#     if request.method == 'POST':
#         memberForm = LoginForm(request.POST)
#         if memberForm.is_valid():
#             email = memberForm.cleaned_data['email']
#             password = memberForm.cleaned_data['password']
#             remember_me = memberForm.cleaned_data['remember_me']
#             user = authenticate(email=email, password=password)

#             if user:
#                 login(request, user)
#                 if not remember_me:
#                     request.session.set_expiry(0)
#                 return redirect('dashboard-page')
#         else:
#             print("Member Form isn't valid")
#     return render(request, 'login_page.html', {'form': memberForm})
