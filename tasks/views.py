from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm
from tasks.models import Employee,Task,TaskDetail,Project
from datetime import date
from django.db.models import Q , Min,Max,Count
# Create your views here.

def manager_dashboard(request):
    return render(request,'dashboard/manager_dashboard.html')
def user_dashboard(request):
    return render(request,'dashboard/user_dashboard.html')

def test(request):
    context = {
        "names" : ["Mahmud", "Ahmed" , "Jhon","Mr. X"],
        "age" : 23
    }
    return render(request, 'test.html',context)

def create_task(request):
    # employee = Employee.objects.all()
    form = TaskModelForm()  #for GET
    if request.method == "POST":
        form = TaskModelForm(request.POST) # for POST
        if form.is_valid():
            
            ''' For Model Form Data '''
            form.save()
            return render(request,'dashboard/task_form.html',{'form':form,'message':'Task Added Successfully'})
    context ={"form": form} 
    return render(request,'dashboard/task_form.html',context)


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
  