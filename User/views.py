from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'user/signupuser.html', {'signup_form': UserCreationForm})
    elif request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('/products/')
            except IntegrityError:
                return render(request, 'user/signupuser.html', {'form': UserCreationForm,
                                                           'error': 'User already taken'})

        else:
            return render(request, 'user/signupuser.html', {'form': UserCreationForm,
                                                       'error': 'Passwords did not match'})
def logoutuser(request):
    if request.method == 'POST': # przegladarki zeby przeyspiszyc dzialanie klikaja w linki zanim w nie klikniesz - tu sie chronimy zeby nie wylogowalo nas samoczynnie
        logout(request)
        return redirect('/')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'user/loginuser.html', {'form': AuthenticationForm})
    elif request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if not user:
            return render(request, 'user/loginuser.html', {'form': AuthenticationForm,
                                                      'error': 'Username or password is not correct'})
        else:
            login(request, user)
            return redirect('/products/')