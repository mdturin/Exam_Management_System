import email
from django import forms
from account.models import *


class MemberForm(forms.Form):
    email = forms.EmailField(required=True)

    password = forms.CharField(required=True)

    remember_me = forms.BooleanField(required=False, initial=False)
