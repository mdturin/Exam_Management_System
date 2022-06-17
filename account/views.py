from django.http import HttpResponse
from django.shortcuts import render
from account.forms import *
from account.models import *


def login_page(request):
    memberForm = MemberForm()
    if request.method == 'POST':
        memberForm = MemberForm(request.POST)
        if memberForm.is_valid():
            print(memberForm.cleaned_data)
            pass
        else:
            print("Member Form isn't valid")
    return render(request, 'login_page.html')
