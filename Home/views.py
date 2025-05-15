from django.shortcuts import render
from .models import Task
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from .forms import TaskForm,UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
# Create your views here.
def task_list(request):
    query = request.GET.get('q')
    if query:
        tasks = Task.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    else:
        tasks = Task.objects.all()

    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST,request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
        pass
    else:
        form = TaskForm()
    return render(request,'task_form.html',{'form':form})

@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task,pk = task_id, user = request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES,instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
        pass
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html',{'form':form})

@login_required
def task_delete(request,task_id):
    task = get_object_or_404(Task,pk = task_id, user = request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request,'task_delete.html',{'task':task})
        
def task_detail(request, task_id):
    task = get_object_or_404(Task,pk = task_id,user = request.user)
    return render(request,'task_detail.html',{'task':task})

# registration
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create a new user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            # Log in the user
            login(request, user)
            # Redirect to tweet list
            return redirect('tweet_list')  # Adjust this if needed
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


