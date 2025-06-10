from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.timezone import now
from django.db import IntegrityError
from datetime import datetime, date
from .models import *
from .forms import *

def is_gerente(user):
    return user.groups.filter(name="Gerente").exists()

def Homepage(request):
    context = {}
    dados_home = homepage.objects.all()
    context['dados_home'] = dados_home
    return render(request, 'homepage.html', context)

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Login realizado com sucesso! Bem-vindo, {user.username}. ✅")
            return redirect('homepage')
        else:
            messages.error(request, "Usuário ou senha inválida. ❌")
            return render(request, 'login.html')
    return render(request, 'login.html')

@login_required
def alt_status(request):
    if request.method == 'POST':
        quarto_id = request.POST.get('quarto_id')
        data_reserva = request.POST.get('data_reserva')

        if not quarto_id or not data_reserva:
            return JsonResponse({'success': False, 'error': 'Parâmetros ausentes.'})

        try:
            quarto_obj = quarto.objects.get(id=quarto_id)
            data_reserva = datetime.strptime(data_reserva, "%Y-%m-%d").date()

            if data_reserva < date.today():
                return JsonResponse({'success': False, 'error': 'Não é possível reservar para datas passadas.'})

            reserva = Reserva.objects.create(quarto=quarto_obj, data=data_reserva)
            return JsonResponse({'success': True})
        except IntegrityError:
            return JsonResponse({'success': False, 'error': 'Este quarto já está reservado nesta data.'})
        except quarto.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Quarto não encontrado.'})
    return JsonResponse({'success': False, 'error': 'Método inválido.'})

@login_required
def cancelar_reserva(request):
    if request.method == 'POST':
        reserva_id = request.POST.get('reserva_id')
        try:
            reserva = Reserva.objects.get(id=reserva_id)
            reserva.delete()
            messages.success(request, "Reserva cancelada com sucesso!")
        except Reserva.DoesNotExist:
            messages.error(request, "Reserva não encontrada.")
    return redirect('reservas')

@login_required
def excluir_reservas_antigas(request):
    if request.method == 'POST':
        hoje = date.today()
        reservas_antigas = Reserva.objects.filter(data__lt=hoje)
        count = reservas_antigas.count()
        reservas_antigas.delete()
        messages.success(request, f'{count} reserva(s) anterior(es) a hoje foram excluídas com sucesso. 🗑️')
        return redirect('reservas')
    return redirect('reservas')

@login_required
def verQuartos(request):
    hoje = date.today()

    quartos = quarto.objects.all().prefetch_related('reservas')

    for q in quartos:
        q.reservas_ativas = q.reservas.filter(data__gte=hoje)
        print(f"Quarto {q.num_Quarto}: {list(q.reservas_ativas)}")

    context = {
        'quartos': quartos,
        'today': hoje.isoformat(),
    }
    return render(request, 'quartos.html', context)

@login_required
def reservas(request):
    reservas = Reserva.objects.select_related('quarto').all()
    context = {'reservas': reservas}
    return render(request, 'reservas.html', context)

from datetime import date

@login_required
@user_passes_test(is_gerente, login_url='homepage')
def addQuarto(request):
    if request.method == 'POST':
        form = quartoForms(request.POST, request.FILES)        
        if form.is_valid():
            novo_quarto = form.save()
            status = form.cleaned_data.get('status')
            data_reserva = form.cleaned_data.get('data_reserva')

            if status == 'False' and data_reserva:
                if data_reserva < date.today():
                    messages.error(request, "Não é possível cadastrar uma reserva em uma data passada. ❌")
                    novo_quarto.delete()
                    return redirect('addQuarto')

                try:
                    Reserva.objects.create(quarto=novo_quarto, data=data_reserva)
                    messages.success(request, "Quarto e reserva cadastrados com sucesso! ✅")
                except IntegrityError:
                    messages.warning(request, "Quarto cadastrado, mas já havia uma reserva para essa data. ❕")
            else:
                messages.success(request, "Quarto cadastrado com sucesso! ✅")

            return redirect('addQuarto')
        else:
            messages.error(request, "Erro ao cadastrar quarto. Verifique os dados e tente novamente. ❌")
    else:    
        form = quartoForms()
    context = {'form': form}
    return render(request, 'addQuartos.html', context)

@login_required
@user_passes_test(is_gerente, login_url='homepage')
def removerQuarto(request):
    if request.method == 'POST':
        quarto_id = request.POST.get('id')
        try:
            q = quarto.objects.get(id=quarto_id)
            q.delete()
            messages.success(request, f"Quarto {q.num_Quarto} removido com sucesso! 🗑️")
        except quarto.DoesNotExist:
            messages.error(request, "Quarto não encontrado. ❌")
        return redirect('removerQuarto')
    quartos = quarto.objects.all()
    context = {'quartos': quartos}
    return render(request, 'rmvQuartos.html', context)

@login_required
@user_passes_test(is_gerente, login_url='homepage')
def add_colaborador(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, '❌ Usuário já existe!')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            funcionario_group, created = Group.objects.get_or_create(name='Funcionarios')
            user.groups.add(funcionario_group)
            user.save()
            messages.success(request, f'✅ Colaborador {username} cadastrado com sucesso!')
            return redirect('addColaborador')

    return render(request, 'addColaborador.html')

@login_required
def Sair(request):
    logout(request)
    messages.success(request, "Logout realizado com sucesso! 👋")
    return redirect('homepage')