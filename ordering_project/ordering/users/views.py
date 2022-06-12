from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from rest_framework import status

from .forms import UserCreationForm, UserLoginForm
from .models import User


@login_required(login_url='users:login')
def users_list_view(request):
    if request.method == 'GET':
        users = User.objects.all()
        return render(request, 'users/users_list.html', {'users': users})


@login_required(login_url='users:login')
def user_detail_view(request, pk):
    if request.method == 'GET':
        if request.user.pk == pk or request.user.is_admin:
            user = User.objects.get(pk=pk)
            return render(request, 'users/user_detail.html', {'user': user})
        else:
            messages.error(request, 'Cant access another profiles info')
            return redirect('users:list')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account has been created for {username}')
            return redirect('users:login')

    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.save()

            if user is not None:
                login(request, user)
                messages.success(request, f'Successfully logged in')

                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('home_page')

            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)

    messages.success(request, f'Successfully logged out')
    return redirect('users:login')
