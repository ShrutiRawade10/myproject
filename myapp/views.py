from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from datetime import date, timedelta
import json
from .models import Task
from .forms import TaskForm


# Create your views here.
def task_list(request):
    tasks = Task.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Filter functionality
    filter_name = None
    filter_param = request.GET.get('filter', '')
    if filter_param == 'pending':
        tasks = tasks.filter(completed=False)
        filter_name = 'Pending Tasks'
    elif filter_param == 'completed':
        tasks = tasks.filter(completed=True)
        filter_name = 'Completed Tasks'

    # Sorting
    sort_param = request.GET.get('sort', '')
    if sort_param == 'due_date':
        tasks = tasks.order_by('due_date')
    elif sort_param == 'priority':
        tasks = tasks.order_by('-priority')
    else:
        tasks = tasks.order_by('-created_at')

    # Statistics
    context = {
        'tasks': tasks,
        'filter_name': filter_name,
        'search_query': search_query,
        'total_tasks': Task.objects.count(),
        'pending_tasks': Task.objects.filter(completed=False).count(),
        'completed_tasks': Task.objects.filter(completed=True).count(),
        'due_soon_tasks': Task.objects.filter(
            due_date__range=[date.today(), date.today() + timedelta(days=3)],
            completed=False
        ).count(),
    }
    
    return render(request, 'task_list.html', context)

@require_POST
def toggle_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    data = json.loads(request.body)
    task.completed = data.get('completed', False)
    task.save()
    return JsonResponse({'status': 'success'})

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form, 'title': 'Create Task'})

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form, 'title': 'Update Task'})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    messages.success(request, 'Task deleted successfully!')
    return redirect('task_list')

