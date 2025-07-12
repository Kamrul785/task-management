from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm, TaskDetailModelForm
from tasks.models import Employee,Task,TaskDetail,Project
from datetime import date
from django.db.models import Q , Min,Max,Count
from django.contrib import messages
# Create your views here.

def manager_dashboard(request):
    type = request.GET.get('type', 'all')
    print(type)
    
    counts = Task.objects.aggregate(
        total = Count('id'),
        completed_task = Count('id', filter=Q(status= "COMPLETED")),
        in_progress_task = Count('id', filter=Q(status= "IN_PROGRESS")),
        pending_task = Count('id', filter=Q(status= "PENDING")),
    )
    
    # Retriving task data 
    base_query = Task.objects.select_related('details').prefetch_related('assigned_to')
    
    if type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type == 'in_progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type == 'pending':
        tasks = base_query.filter(status='PENDING')
    elif type == 'all':
        tasks = base_query.all()
        
    
    
    context = {
        "tasks":tasks,
        "counts" : counts
    }
    return render(request,'dashboard/manager_dashboard.html' , context)

def user_dashboard(request):
    return render(request,'dashboard/user_dashboard.html')

def test(request):
    context = {
        "names" : ["Mahmud", "Ahmed" , "Jhon","Mr. X"],
        "age" : 23
    }
    return render(request, 'test.html',context)

""" CURD operations """
def create_task(request):
    task_form = TaskModelForm()  #for GET
    task_detail_form = TaskDetailModelForm()
    
    if request.method == "POST":
        task_form = TaskModelForm(request.POST) # for POST
        task_detail_form = TaskDetailModelForm(request.POST) # for POST
        if task_form.is_valid() and task_detail_form.is_valid():
            ''' For Model Form Data '''
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            
            messages.success(request, "Task Created Successfully ")
            return redirect('create_task')
    print(task_form)
    context = {"task_form": task_form, "task_detail_form" : task_detail_form} 
    return render(request,'dashboard/task_form.html',context)


def update_task(request,id):
    task = Task.objects.get(id = id)
    task_form = TaskModelForm(instance = task)  #for GET
    
    if task.details:
        task_detail_form = TaskDetailModelForm(instance = task.details)
    
    if request.method == "POST":
        task_form = TaskModelForm(request.POST, instance = task) # for POST
        task_detail_form = TaskDetailModelForm(request.POST, instance = task.details) # for POST
        if task_form.is_valid() and task_detail_form.is_valid():
            ''' For Model Form Data '''
            task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            
            messages.success(request, "Task Updated Successfully ")
            return redirect('update_task' , id )
    print(task_form)
    context = {"task_form": task_form, "task_detail_form" : task_detail_form} 
    return render(request,'dashboard/task_form.html',context)


def delete_task(request,id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request,"Task Deleted Successfully")
        return redirect('manager_dashboard')
    else:
        messages.error(request,"Something Went Wrong")
        return redirect('manager_dashboard')

def view_task(request):
    # show the task that are completed
    # tasks = Task.objects.filter(status='PENDING')
    
    # show the task which due date is today 
    # tasks = Task.objects.filter(due_date = date.today())
    
    """Show the task whose priority is not low"""
    # tasks = TaskDetail.objects.exclude(priority = 'L')
    
    """ Show the task which are pending or in process """
    # tasks = Task.objects.filter(Q(status = "PENDING") | Q(status = 'IN_PROGRESS'))

    """ Select_related (Foreignkey, OneToOneField)  2 way"""
    # tasks = Task.objects.select_related('details').all()    # way 1
    # tasks = TaskDetail.objects.select_related('task').all()   # way 2
    # for foreign key 
    # tasks = Task.objects.select_related('project').all()
    
    """ prefetch_related (reverse ForeignKey, manyToMany)"""
    # tasks = Project.objects.prefetch_related('task_set').all()
    
    # access employee from task
    # tasks = Task.objects.prefetch_related('assigned_to').all()
    
    # access task form employee (project theke taks k access korar moto)
    # tasks = Employee.objects.prefetch_related('tasks').all()
    
    # Aggregation 
    # task_count = Task.objects.aggregate(num_task = Count('id'))
    
    # Annotate
    projects = Project.objects.annotate(num_task = Count('task')).order_by('num_task')
    
    return render(request,'show_task.html', {'projects':projects})

