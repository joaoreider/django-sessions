from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Usuario
from hashlib import sha256

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

    # Nome e email não podem ser nulos
    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        return redirect('/auth/cadastro/?status=1')
    
    if len(senha) < 8:
        return redirect('/auth/cadastro/?status=2')

    # Verifica se o usuário já existe no sistema
    usuario = Usuario.objects.filter(email = email)

    if len(usuario) > 0:
        return redirect('/auth/cadastro/?status=3')

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
        return redirect('/auth/cadastro/?status=0')
    
    except:
        return redirect('/auth/cadastro/?status=4')

def valida_login(request):
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    # Criptografia sha256 na senha
    senha = sha256(senha.encode()).hexdigest()

    # Verifica se existe o usuário digitado 
    usuario = Usuario.objects.filter(email = email).filter(senha=senha)
    if len(usuario) == 0:
        return redirect('/auth/login/?status=1')
    elif len(usuario) > 0:
        request.session['logado'] = True
        request.session['usuario_id'] = usuario[0].id
        return redirect('/plataforma/home')


    return HttpResponse(f"{email}  {senha}")

def sair(request):
    request.session.flush()
    return redirect('/auth/login')