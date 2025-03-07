from django.core.signals import request_started
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Task
from account.models import User
from .forms import CreateTaskForm
from django.db.models import Q


@login_required()
def task_list(request):
    tasks = request.user.tasks.all().order_by('deadline')
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
    print(f"Task found: {task.title}, {task.deadline}, {task.status}")
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
    task.delete()
    return redirect('home')


@login_required()
def home(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'deadline')

    tasks = Task.objects.all()

    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(status__icontains=query) |
            Q(priority__icontains=query)
        )

    tasks = tasks.order_by(sort_by)

    status = request.GET.get('status')
    priority = request.GET.get('priority')
    deadline = request.GET.get('deadline')

    if status:
        tasks = tasks.filter(status=status)
    if priority:
        tasks = tasks.filter(priority=priority)
    if deadline:
        today = timezone.now().date()  # Get current date only
        if deadline == 'overdue':
            tasks = tasks.filter(deadline__date__lt=today)
        elif deadline == 'today':
            tasks = tasks.filter(deadline__date=today)
        elif deadline == 'week':
            week_end = today + timezone.timedelta(days=7)
            tasks = tasks.filter(deadline__date__gte=today, deadline__date__lt=week_end)

    if sort_by in ['deadline', 'priority', 'status', 'created_at']:
        tasks = tasks.order_by(sort_by)
    elif sort_by == '-deadline':  # Allow descending order for deadline
        tasks = tasks.order_by('-deadline')

    context = {'tasks': tasks,
               'status_filter': request.GET.get('status'),
               'priority_filter': request.GET.get('priority'),
               'deadline_filter': request.GET.get('deadline'),
               'sort_by': request.GET.get('sort', 'deadline'),
               'now': timezone.now()
               }
    return render(request, 'tasks/index.html', context)
