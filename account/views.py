from django.shortcuts import render
from django.contrib.auth.models import User

from account.forms import *
from account.mail_sender import send_code
from account.models import *


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

    return render(request, 'register_page.html', context)
