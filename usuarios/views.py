from receitas.models import Receita
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User

def cadastro(request):
  if request.method == 'POST':
    nome = request.POST['nome']
    email = request.POST['email']
    senha = request.POST['password']
    senha2 = request.POST['password2']

    if campo_vazio(nome) or campo_vazio(email) or campo_vazio(senha):
      messages.error(request, 'Os campos NOME, EMAIL e/ou SENHA não podem ficar em branco')
      return redirect('cadastro')
    if confirma_senha(senha, senha2):
      messages.error(request, 'As senhas devem ser iguais')
      return redirect('cadastro')
    if User.objects.filter(username = nome).exists():
      messages.error(request, 'NOME de usuário já cadastrado')
      return redirect('cadastro')
    if User.objects.filter(email = email).exists():
      messages.error(request, 'EMAIL já cadastrado')
      return redirect('cadastro')

    user = User.objects.create_user(
      username = nome,
      email = email,
      password = senha
    )

    user.save()

    messages.success(request, 'Usuário cadastrado com sucesso')
    return redirect('login')
  else:
    return render(request, 'usuarios/cadastro.html')

def login(request):
  if request.method == 'POST':
    email = request.POST['email']
    senha = request.POST['senha']

    if campo_vazio(email) or campo_vazio(senha):
      messages.error(request, 'Email e/ ou senha inválidos. Tente novamente :)')
      return redirect('login')

    if User.objects.filter(email = email).exists():
      nome = User.objects.filter(email = email).values_list('username', flat = True).get()
      user = auth.authenticate(request, username = nome, password = senha)
      if user is not None:
        auth.login(request, user)
        messages.success(request, 'Login realizado com sucesso!')
        return redirect('dashboard')
      else:
        messages.error(request, 'Email e/ ou senha inválidos. Tente novamente :)')

  return render(request, 'usuarios/login.html')

def logout(request):
  auth.logout(request)
  return redirect('index')

def dashboard(request):
  if request.user.is_authenticated:
    id = request.user.id
    recepies = Receita.objects.order_by('-date_receita').filter(pessoa = id)

    data = {
      'receitas': recepies
    }

    return render(request, 'usuarios/dashboard.html', data)
  else:
    return redirect('index')

def criar_receita(request):
  if request.method == 'POST':
    nome_receita = request.POST['nome_receita']
    ingredientes = request.POST['ingredientes']
    modo_preparo = request.POST['modo_preparo']
    tempo_preparo = request.POST['tempo_preparo']
    rendimento = request.POST['rendimento']
    categoria = request.POST['categoria']
    foto_receita = request.FILES['foto_receita']

    user = get_object_or_404(User, pk = request.user.id)

    receita = Receita.objects.create(
      nome_receita = nome_receita,
      ingredientes = ingredientes,
      modo_preparo = modo_preparo,
      tempo_preparo = tempo_preparo,
      rendimento = rendimento,
      categoria = categoria,
      foto_receita = foto_receita,
      pessoa = user,
    )

    receita.save()
    return redirect('dashboard')
  else:
    return render(request, 'usuarios/criar_receita.html')

def campo_vazio(campo):
  return not campo.strip()

def confirma_senha(senha, confirmacao):
  return senha != confirmacao
