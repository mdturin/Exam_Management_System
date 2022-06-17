from django.http import HttpResponse
from django.shortcuts import render


def login_page(request):
    return render(request, 'login_page.html')
