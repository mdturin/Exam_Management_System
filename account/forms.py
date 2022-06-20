from django import forms
from django.contrib.auth.models import User

from account.models import *

TEACHER_TITLE_CHOICES = [
    ('', ''),
    ('Professor', 'Professor'),
    ('Associate Professor', 'Associate Professor'),
    ('Assistant Professor', 'Assistant Professor'),
    ('Lecturer', 'Lecturer'),
    ('None', 'None'),
]


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.PasswordInput()
    remember_me = forms.BooleanField()


class UserRegistraionForm(forms.ModelForm):

    first_name = forms.CharField(required=True)

    last_name = forms.CharField(required=True)

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'is_staff',
            'email',
            'password'
        ]
        widgets = {
            'password': forms.PasswordInput()
        }


class MemberRegisterForm(forms.ModelForm):

    contact_number = forms.CharField(
        required=True, max_length=11, min_length=11, strip=True)

    class Meta:
        model = Member
        fields = [
            'is_dean',
            'is_teacher',
            'title',
            'contact_number',
            'profile_picture',
        ]

        widgets = {
            'title': forms.Select(choices=TEACHER_TITLE_CHOICES),
        }
