from django import forms
from django.contrib.auth.forms import UserCreationForm

from account.choices import *
from account.models import *


class MemberLoginForm(forms.Form):

    email = forms.EmailField(required=True)

    password = forms.CharField(required=True)

    remember_me = forms.BooleanField(required=False, initial=False)


class MemberRegisterForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'is_dean',
            'is_teacher',
            'is_staff',
        ]

        widgets = {
            'is_dean': forms.CheckboxInput(),
            'is_teacher': forms.CheckboxInput(),
            'is_staff': forms.CheckboxInput(),
        }
