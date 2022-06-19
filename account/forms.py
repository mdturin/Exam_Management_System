from django import forms
from account.choices import *
from account.models import *
from account.validator import *


class MemberLoginForm(forms.Form):

    email = forms.EmailField(required=True)

    password = forms.CharField(required=True)

    remember_me = forms.BooleanField(required=False, initial=False)


class MemberRegisterForm(forms.ModelForm):

    first_name = forms.CharField(required=True)

    last_name = forms.CharField(required=True)

    email = forms.EmailField(required=True)

    contact_number = forms.CharField(
        required=True, max_length=11, min_length=11, strip=True, validators=[contact_number_validator])

    class Meta:
        model = Member
        fields = [
            'email',
            'first_name',
            'last_name',
            'password',
            'is_dean',
            'is_teacher',
            'is_staff',
            'title',
            'contact_number',
        ]

        widgets = {
            'is_dean': forms.CheckboxInput(),
            'is_teacher': forms.CheckboxInput(),
            'is_staff': forms.CheckboxInput(),
            'title': forms.Select(choices=TEACHER_TITLE_CHOICES),
            'password': forms.PasswordInput(),
        }
