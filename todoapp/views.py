from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import ToDoList
from django.utils import timezone


def home(request):
    return render(request, 'todoapp/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todoapp/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todoapp/signupuser.html',
                       {'form': UserCreationForm(), 'error': 'This username is already taken. Please choose another one'})
        else:
            return render(request, 'todoapp/signupuser.html', {'form': UserCreationForm(), 'error': 'Passwords did not match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todoapp/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todoapp/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username or password is incorrect'})
        else:
            login(request, user)
            return redirect('currenttodos')


def currenttodos(request):
    todos = ToDoList.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todoapp/currenttodos.html', {'todos': todos})


def viewtodo(request, todo_pk):
    todo = get_object_or_404(ToDoList, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todoapp/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todoapp/viewtodo.html', {'todo': todo, 'form': form, 'error': 'Bad data'})


def completetodo(request, todo_pk):
    todo = get_object_or_404(ToDoList, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')


def deletetodo(request, todo_pk):
    todo = get_object_or_404(ToDoList, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todoapp/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todoapp/createtodo.html', {'form': TodoForm(), 'error': 'Bad data passed in'})
