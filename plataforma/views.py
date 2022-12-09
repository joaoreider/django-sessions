from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='/auth/login')
def home(request):
    return render(request, 'home.html')
 
