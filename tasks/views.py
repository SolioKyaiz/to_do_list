from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.core.signals import request_started
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import title
from django.utils import timezone
from .models import Task
from account.models import User
from .forms import CreateTaskForm
from django.db.models import Q
from datetime import timedelta


@login_required()
def task_list(request):
    tasks = request.user.tasks.all().order_by('deadline')
    print(tasks)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


@login_required()
def task_create(request):
    if request.method == "POST":
        form = CreateTaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.created_at = timezone.now()
            task.save()
            return redirect('home')
    else:
        form = CreateTaskForm(user=request.user)
    return render(request, 'tasks/task_create.html', {'form': form})


@login_required()
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == "POST":
        form = CreateTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CreateTaskForm(instance=task)
    return render(request, 'tasks/task_edit.html', {'form': form, 'task': task})


@login_required()
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('home')
    return render(request,'tasks/task_confirm_delete.html', {'task': task})


@login_required()
def home(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    priority = request.GET.get('priority', '')
    deadline = request.GET.get('deadline', '')

    tasks = Task.objects.filter(owner=request.user)

    if query:
        tasks = tasks.filter(title__icontains=query)
    if status and status != '':
        tasks = tasks.filter(status=status)
    if priority and priority != '':
        tasks = tasks.filter(priority=priority)
    if deadline and deadline != '':
        today = timezone.now().date()
        if deadline == 'overdue':
            tasks = tasks.filter(deadline__lt=today, deadline__isnull=False)
        elif deadline == 'today':
            tasks = tasks.filter(deadline=today)
        elif deadline == 'next_week':
            next_week = today + timedelta(days=7)
            tasks = tasks.filter(deadline__range=(today, next_week))

    return render(request, 'tasks/index.html', {
        'tasks': tasks,
        'query': query,
        'status': status,
        'priority': priority,
        'deadline': deadline,
    })

@login_required()
def completed_tasks(request):
    query = request.GET.get('q','')
    if query:
        complete_tasks = Task.objects.filter(status='Done',title__icontains=query)
    else:
        complete_tasks = Task.objects.filter(status='Done')

    return render(request,'tasks/completed_tasks.html',{'complete_tasks':complete_tasks})

