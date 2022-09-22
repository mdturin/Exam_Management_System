from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from account.forms import *
from account.mail_sender import send_code
from account.models import *

# login auth
from django.contrib import messages

from dashboard.views import *

def login_code(request):
    context = {'title': 'Verify User'}
    if request.method == 'POST':
        email = request.POST.get('set-email', '')
        code = request.POST.get('text', '')
        user = User.objects.get(email=email)
        otp_user = OTP.objects.get(user=user)
        if otp_user.code == code:
            return redirect('set-password')
        else:
            messages.warning(request, ("Code didn't match"))
            # context['code-error'] = "Code didn't match"
    return render(request, 'login_code.html', context)


def set_password(request):
    context = {'title': 'Set Password'}
    if request.method == 'POST':
        email = request.POST.get('set-email', '')
        pass1 = request.POST.get('password1', '')
        pass2 = request.POST.get('password2', '')

        user = User.objects.get(email=email)
        if pass1 == pass2:
            user.set_password(pass1)
            user.save()
        else:
            messages.warning(request, ("Passwords didn't match"))
            # context['pass-error'] = "passwords didn't match"
            render(request, 'set_password.html', context)

        user = authenticate(request, username=email, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('dashboard-page')
        else:
            # Maybe this section has some problems
            pass
            # messages.warning(request, ("System Fail. Try Again!"))
            # context['error'] = 'System Fail. Try Again!'

    return render(request, 'set_password.html', context)


def register_page(request):

    context = {'title': 'Sign Up'}

    if request.method == 'POST':
        email = request.POST.get('email', '')

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            # print(email, 'dosent exist')
            messages.warning(request, (email+ ' dosent exist'))
            return render(request, 'register_page.html', context)

        code = send_code(email)

        try:
            otp_user = OTP.objects.get(user=user)
            otp_user.code = code
            otp_user.save()
        except OTP.DoesNotExist:
            otp_user = OTP.objects.create(user=user, code=code)

        return redirect('login-code')

    return render(request, 'register_page.html', context)

def home(request):
    return render(request, 'home.html')
