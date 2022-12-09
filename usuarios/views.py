from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Usuario
from hashlib import sha256
from django.contrib import messages, auth
from django.contrib.auth.models import User

def login(request):
    status = request.GET.get('status')
    return render(request, 'login.html', {'status':status})

def cadastro(request):
    # Recebe o status da url
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status':status})

def valida_cadastro(request):
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    
    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        messages.add_message(request, messages.constants.ERROR, 'Nome e email não podem ser nulos')
        return redirect('/auth/cadastro/')
    
    if len(senha) < 8:
        messages.add_message(request, messages.constants.ERROR, 'Sua senha deve ter no mínimo 8 caracteres')
        return redirect('/auth/cadastro/')

    if User.objects.filter(email=email).exists():
        messages.add_message(request, messages.constants.ERROR, 'Email já cadastrado no sistema')
        return redirect('/auth/cadastro/')
    
    if User.objects.filter(username=nome).exists():
        messages.add_message(request, messages.constants.ERROR, 'Nome já cadastrado no sistema')
        return redirect('/auth/cadastro/')

    try:
        usuario = User.objects.create_user(username=nome, email=email, password=senha)
        usuario.save()
        messages.add_message(request, messages.constants.SUCCESS, 'Cadastro efetuado com sucesso')
        return redirect('/auth/cadastro/')
    
    except:
        messages.add_message(request, messages.constants.ERROR, 'Erro interno do sistema')
        return redirect('/auth/cadastro/')

def valida_login(request):
    nome = request.POST.get('nome')
    senha = request.POST.get('senha')

    usuario = auth.authenticate(request, username = nome, password = senha)
    if not usuario:
        messages.add_message(request, messages.constants.WARNING, 'Email ou senha inválido')
        return redirect('/auth/login/')
    else:
        auth.login(request, usuario)

        return redirect('/plataforma/home')


def sair(request):
    auth.logout(request)
    messages.add_message(request, messages.constants.WARNING, 'Faça o login antes de acessar a plataforma')
    return redirect('/auth/login')