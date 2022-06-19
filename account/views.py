from django.http import HttpResponse
from django.shortcuts import render
from account.forms import *
from account.models import *


def login_page(request):
    memberForm = MemberLoginForm()
    if request.method == 'POST':
        memberForm = MemberLoginForm(request.POST)
        if memberForm.is_valid():
            print(memberForm.cleaned_data)
            pass
        else:
            print("Member Form isn't valid")
    return render(request, 'login_page.html', {'form': memberForm})


def register_page(request):
    memberForm = MemberRegisterForm()
    formErrors = ''

    if request.method == 'POST':
        memberForm = MemberRegisterForm(request.POST)
        if memberForm.is_valid():
            print(memberForm.cleaned_data)
        else:
            print("Member Form isn't valid")
            formErrors = memberForm.errors.as_json()
            print(formErrors)

    return render(request, 'register_page.html', {
        'form': memberForm,
        'errors': formErrors
    })
