from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from django.shortcuts import render, redirect
from .models import Task, Profile
from .forms import TaskForm


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()
        Profile.objects.create(user=user)
        return redirect('login')
    else:
        return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('task_view')
        else:
            return HttpResponse('Invalid login')
    else:
        return render(request, 'login.html')


def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})


def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.profile = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})


def task_view(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
        code = Profile.objects.get(user=request.user).code
        return render(request, 'task.html', {'tasks': tasks, 'username': request.user.username, 'code': code})
    else:
        return redirect('login')


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_view')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})


def task_update(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_view')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form})


def task_delete(request, pk):
    Task.objects.get(pk=pk).delete()
    return redirect('task_view')


def user_logout(request):
    logout(request)
    return redirect('home')


def home(request):
    return render(request, 'base.html')


