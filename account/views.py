from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic.base import TemplateView

from account.forms import *
from account.mail_sender import send_code
from account.models import *


class LoginCodeView(TemplateView):
    template_name = "login_code.html"


class SetPasswordView(TemplateView):
    template_name = "set_password.html"


def register_page(request):

    context = {'title': 'Sign Up'}

    if request.method == 'POST':
        email = request.POST.get('email', '')

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            print(email, 'dosent exist')
            return render(request, 'register_page.html', context)

        code = send_code(email)

        try:
            otp_user = OTP.objects.get(user=user)
            otp_user.code = code
            otp_user.save()
        except OTP.DoesNotExist:
            otp_user = OTP.objects.create(user=user, code=code)

        context = {'title': 'Verify User'}
        return render(request, 'login_code.html', context)

    return render(request, 'register_page.html', context)
