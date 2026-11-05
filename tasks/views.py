from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Task, Subject
from django.utils import timezone
from .forms import TaskForm, SubjectForm
from datetime import timedelta

@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='completed').count()
    pending_tasks = tasks.filter(status='pending').count()
    
    today = timezone.now().date()
    overdue_tasks = tasks.filter(due_date__lt=today).exclude(status='completed').count()
    upcoming_deadlines = tasks.exclude(status='completed').order_by('due_date')[:5]
    
    start_of_week = today - timedelta(days=today.weekday())
    chart_data = []
    for i in range(7):
        day_date = start_of_week + timedelta(days=i)
        count = tasks.filter(created_at__date=day_date).count()
        chart_data.append(count)
    
    max_count = max(chart_data) if max(chart_data) > 0 else 1
    
    # DYNAMIC GREETING LOGIC
    current_hour = timezone.now().hour
    if current_hour < 12:
        greeting = "Good morning"
    elif current_hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
        'upcoming_deadlines': upcoming_deadlines,
        'chart_data': chart_data,
        'max_count': max_count,
    }
    return render(request, 'tasks/dashboard.html', context)

@login_required
def my_tasks(request):
    tasks = Task.objects.filter(user=request.user).order_by('due_date')
    subjects = Subject.objects.filter(user=request.user)
    context = {
        'tasks': tasks,
        'subjects': subjects,
    }
    return render(request, 'tasks/my-tasks.html', context) 

@login_required
def calendar(request):
    tasks = Task.objects.filter(user=request.user)
    context = {
        'tasks': tasks,
    }
    return render(request, 'tasks/calendar.html', context) 

@login_required
def subjects(request):
    subjects = Subject.objects.filter(user=request.user)
    context = {
        'subjects': subjects,
    }
    return render(request, 'tasks/subjects.html', context)

@login_required
def settings(request):
    context = {
        'user': request.user,
    }
    return render(request, 'tasks/settings.html', context)

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user 
            task.save()
            messages.success(request, "Task added successfully!")
            return redirect('my_tasks') 
    else:
        form = TaskForm()
    
    context = {
        'form': form,
    }
    return render(request, 'tasks/add-task.html', context)

@login_required
def edit_task(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    if request.method == 'POST':
       task.title = request.POST.get('title')
       task.description = request.POST.get('description')
       task.task_type = request.POST.get('task_type')
       task.priority = request.POST.get('priority')
       task.due_date = request.POST.get('due_date')
       task.status = request.POST.get('status')

       subject_id = request.POST.get('subject')
       if subject_id:
           task.subject = Subject.objects.get(id=subject_id, user=request.user)

       task.save()
       messages.success(request, "Task updated successfully!")
       return redirect('my_tasks')

    subjects = Subject.objects.filter(user=request.user)
    context = {
        'task': task,
        'subjects': subjects,
    }
    return render(request, 'tasks/edit-task.html', context)

@login_required
def delete_task(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, "Task deleted successfully!")
        return redirect('my_tasks')
    return redirect('my_tasks')

@login_required
def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            messages.success(request, "Subject added successfully!")
            return redirect('subjects')
    else:
        form = SubjectForm()
    return render(request, 'tasks/add-subject.html', {'form': form})

@login_required
def edit_subject(request, pk):
    subject = Subject.objects.get(id=pk, user=request.user)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, "Subject updated successfully!")
            return redirect('subjects')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'tasks/edit-subject.html', {'form': form, 'subject': subject})

@login_required
def delete_subject(request, pk):
    subject = Subject.objects.get(id=pk, user=request.user)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, "Subject deleted successfully!")
        return redirect('subjects')
    return redirect('subjects')

@login_required
def toggle_task(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    if task.status == 'completed':
        task.status = 'pending'
        messages.success(request, "Task marked as Pending.")
    else:
        task.status = 'completed'
        messages.success(request, "Task marked as Completed!")
    task.save()
    return redirect('my_tasks')

# --- REGISTER VIEW (Walang @login_required) ---
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'tasks/register.html', {'form': form})