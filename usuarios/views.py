from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Usuario
from hashlib import sha256
from django.contrib import messages

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

    # Verifica se o usuário já existe no sistema
    usuario = Usuario.objects.filter(email = email)

    if len(usuario) > 0:
        messages.add_message(request, messages.constants.ERROR, 'Email já cadastrado no sistema')
        return redirect('/auth/cadastro/')

    try:
        # Criptografia sha256 na senha
        senha = sha256(senha.encode()).hexdigest()

        # Cadastra no bancod e dados
        usuario = Usuario(
            nome = nome,
            senha = senha,
            email = email
        )
        usuario.save()
        messages.add_message(request, messages.constants.SUCCESS, 'Cadastro efetuado com sucesso')
        return redirect('/auth/cadastro/')
    
    except:
        messages.add_message(request, messages.constants.ERROR, 'Erro interno do sistema')
        return redirect('/auth/cadastro/')

def valida_login(request):
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    # Criptografia sha256 na senha
    senha = sha256(senha.encode()).hexdigest()

    # Verifica se existe o usuário digitado 
    usuario = Usuario.objects.filter(email = email).filter(senha=senha)
    if len(usuario) == 0:
        messages.add_message(request, messages.constants.WARNING, 'Email ou senha inválido')
        return redirect('/auth/login/')
    elif len(usuario) > 0:
        request.session['logado'] = True
        request.session['usuario_id'] = usuario[0].id
        return redirect('/plataforma/home')


def sair(request):
    request.session.flush()
    messages.add_message(request, messages.constants.WARNING, 'Faça o login antes de acessar a plataforma')
    return redirect('/auth/login')