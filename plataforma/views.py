from django.shortcuts import render, redirect
from django.http import HttpResponse

def home(request):
    if request.session.get('logado'):
        return render(request, 'home.html')
    else:
        return redirect('/auth/login/?status=2')
