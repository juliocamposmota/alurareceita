from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User

def cadastro(request):
  if request.method == 'POST':
    nome = request.POST['nome']
    email = request.POST['email']
    senha = request.POST['password']
    senha2 = request.POST['password2']

    if not nome.strip():
      print('O campo NOME não pode ficar em branco')
      return redirect('cadastro')
    if not email.strip():
      print('O campo EMAIL não pode ficar em branco')
      return redirect('cadastro')
    if not senha.strip():
      print('O campo SENHA não pode ficar em branco')
      return redirect('cadastro')
    if senha != senha2:
      print('As senhas devem ser iguais')
      return redirect('cadastro')
    if User.objects.filter(username = nome).exists():
      print('NOME de usuário já cadastrado')
      return redirect('cadastro')
    if User.objects.filter(email = email).exists():
      print('EMAIL já cadastrado')
      return redirect('cadastro')

    user = User.objects.create_user(
      username = nome,
      email = email,
      password = senha
    )

    user.save()

    print('Usuário cadastrado com sucesso')
    return redirect('login')
  else:
    return render(request, 'usuarios/cadastro.html')

def login(request):
  if request.method == 'POST':
    email = request.POST['email']
    senha = request.POST['senha']

    if email == '' or senha == '':
      print('Email e/ ou senha inválidos. Tente novamente :)')
      return redirect('login')

    if User.objects.filter(email = email).exists():
      nome = User.objects.filter(email = email).values_list('username', flat = True).get()
      user = auth.authenticate(request, username = nome, password = senha)
      if user is not None:
        auth.login(request, user)
        print('Login realizado com sucessso!')
        return redirect('dashboard')
      else:
        print('Email e/ ou senha inválidos. Tente novamente :)')

  return render(request, 'usuarios/login.html')

def logout(request):
  auth.logout(request)
  return redirect('index')

def dashboard(request):
  if request.user.is_authenticated:
    return render(request, 'usuarios/dashboard.html')
  else:
    return redirect('index')
