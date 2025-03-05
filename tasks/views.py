from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Task
from account.models import User
from .forms import CreateTaskForm

@login_required()
def task_list(request):
    tasks = request.user.tasks.all().order_by('deadline')
    return render(request,'tasks/task_list.html',{'tasks':tasks})

@login_required()
def task_create(request):
    if request.method == "POST":
        form = CreateTaskForm(request.POST,user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.created_at=timezone.now()
            task.save()
            return redirect('tasks:task-list')
    else:
        form = CreateTaskForm(user=request.user)
    return render(request,'tasks/task_create.html',{'form':form})

@login_required()
def task_edit(request,pk):
    task = get_object_or_404(Task,pk = pk,owner=request.user)
    print(f"Task found: {task.title}, {task.deadline}, {task.status}")
    if request.method == "POST":
        form = CreateTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:task-list')
    else:
        form = CreateTaskForm(instance=task)
    return render(request,'tasks/task_edit.html',{'form':form,'task':task})

@login_required()
def task_delete(request,pk):
    task = get_object_or_404(Task,pk=pk,owner=request.user)
    task.delete()
    return redirect('tasks:task-list')
