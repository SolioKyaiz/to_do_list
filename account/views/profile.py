from django.db.models.fields import return_None
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from account.models import User
from account.forms import ProfileForm
from tasks.models import Task

@login_required
def profile(request):
    user = request.user
    tasks = user.tasks.all()
    return render(request,'account/profile.html',{'user':user,'tasks':tasks})

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('account:profile')
    else:
        form = ProfileForm(instance=user)
        return render(request,'account/edit_profile.html',{'form':form})