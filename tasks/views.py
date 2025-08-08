from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm, TaskDetailModelForm
from tasks.models import Task,TaskDetail,Project
from datetime import date
from django.db.models import Q , Min,Max,Count
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test , login_required ,permission_required
from users.views import is_admin
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin,UserPassesTestMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, DetailView, UpdateView,TemplateView



# class based view example 
class Greetings(View):
    greetings = 'Hellow Everyone'
    
    def get(self,request):
        return HttpResponse(self.greetings)
    
class HiGreetings(Greetings):
    greetings = "Hi there, How are you ? "


# Create your views here.

def is_manager(user):
    return user.groups.filter(name='Manager').exists()
def is_employee(user):
    return user.groups.filter(name='Employee').exists()


@login_required
@user_passes_test(is_manager, login_url='no_permission')
def manager_dashboard(request):
    type = request.GET.get('type', 'all')
    # print(type)
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

def employee_dashboard(request):
    return render(request,'dashboard/user_dashboard.html')

class EmployeeDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'dashboard/user_dashboard.html'
    login_url = 'no_permission'
    
    def test_func(self):
        return is_employee(self.request.user)
    
    
    

""" CURD operations """

@login_required
@permission_required('tasks.add_task', login_url='no_permission')
def create_task(request):
    task_form = TaskModelForm()  #for GET
    task_detail_form = TaskDetailModelForm()
    
    if request.method == "POST":
        task_form = TaskModelForm(request.POST) # for POST
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES) # for POST
        if task_form.is_valid() and task_detail_form.is_valid():
            ''' For Model Form Data '''
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            
            messages.success(request, "Task Created Successfully ")
            return redirect('create_task')
        
    context = {"task_form": task_form, "task_detail_form" : task_detail_form} 
    return render(request,'dashboard/task_form.html',context)

# CBV of create_task

# create_decorators = [login_required, permission_required('tasks.add_task', login_url='no_permission')]
# @method_decorator(create_decorators, name='dispatch')
class CreateTask(ContextMixin,LoginRequiredMixin,PermissionRequiredMixin, View):
    """ For Creating Task """

    permission_required = 'tasks.add_task'
    permission_denied_url = 'no_permission'
    login_url = 'sign_in'
    template_name = 'dashboard/task_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = kwargs.get('task_form', TaskModelForm())
        context['task_detail_form'] = kwargs.get('task_detail_form', TaskDetailModelForm())
        return context
    
    def get(self, request, *args, **kwargs):

        context = self.get_context_data()
        return render(request,self.template_name,context)
    
    def post(self, request, *args, **kwargs):
        task_form = TaskModelForm(request.POST)  
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES) 
        if task_form.is_valid() and task_detail_form.is_valid():
            ''' For Model Form Data '''
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            
            messages.success(request, "Task Created Successfully ")
            return redirect('create_task')     
        
        context = self.get_context_data(task_form=task_form, task_detail_form=task_detail_form)
        return render(request,self.template_name,context)



@login_required
@permission_required('tasks.change_task', login_url='no_permission')
def update_task(request,id):
    task = Task.objects.get(id = id)
    task_form = TaskModelForm(instance = task)  #for GET
    
    if task.details:
        task_detail_form = TaskDetailModelForm(instance = task.details)
    
    if request.method == "POST":
        task_form = TaskModelForm(request.POST, instance = task) # for POST
        task_detail_form = TaskDetailModelForm(request.POST,request.FILES, instance = task.details) # for POST
        if task_form.is_valid() and task_detail_form.is_valid():
            ''' For Model Form Data '''
            task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            
            messages.success(request, "Task Updated Successfully ")
            return redirect('update_task' , id )
    # print(task_form)
    context = {"task_form": task_form, "task_detail_form" : task_detail_form} 
    return render(request,'dashboard/task_form.html',context)



class UpdateTask(UpdateView):
    model = Task
    form_class = TaskModelForm
    template_name = 'dashboard/task_form.html'
    context_object_name = 'task'
    pk_url_kwarg = 'id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = self.get_form()
        print(context)
        if hasattr(self.object, 'details') and self.object.details:
            context['task_detail_form'] = TaskDetailModelForm(instance = self.object.details)
        else:
            context['task_detail_form'] = TaskDetailModelForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_form = TaskModelForm(request.POST, instance = self.object)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES, instance = getattr(self.object, 'details', None))
        if task_form.is_valid() and task_detail_form.is_valid():
            ''' For Model Form Data '''
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            
            messages.success(request, "Task Updated Successfully ")
            return redirect('update_task' , self.object.id )
        return redirect('update_task',self.object.id)



# update_decorators = [login_required, permission_required('tasks.change_task', login_url='no_permission')]
# @method_decorator(update_decorators, name='dispatch')
# class UpdateTask(ContextMixin,LoginRequiredMixin, PermissionRequiredMixin,View):
#     """ For updating Task"""
    
#     template_name = 'dashboard/task_form.html'
#     permission_required = 'tasks.change_task'
#     permission_denied_url = 'no_permission'
#     login_url = 'sign_in'
    
#     def get_context_data(self, **kwargs):
#         context =  super().get_context_data(**kwargs)
#         context['task_form'] = kwargs.get('task_form', TaskModelForm())
#         context['task_detail_form'] = kwargs.get('task_detail_form', TaskDetailModelForm())
#         return context
    
    
#     def get(self,request, *args, **kwargs):
#         task_id = kwargs['id']
#         task = Task.objects.get(id = task_id)
#         task_form = TaskModelForm(instance = task)  #for GET
#         task_detail_form = TaskDetailModelForm()
#         if task.details:
#             task_detail_form = TaskDetailModelForm(instance = task.details)      
#         context = self.get_context_data(task_form=task_form, task_detail_form=task_detail_form)
#         return render(request,self.template_name,context)
    
    
#     def post(self, request, *args, **kwargs):
#         task_id = kwargs['id']
#         task = Task.objects.get(id = task_id)
#         task_form = TaskModelForm(request.POST, instance = task) # for POST
#         task_detail_form = TaskDetailModelForm(request.POST, instance = task.details) # for POST
#         if task_form.is_valid() and task_detail_form.is_valid():
#             ''' For Model Form Data '''
#             task_form.save()
#             task_detail = task_detail_form.save(commit=False)
#             task_detail.task = task
#             task_detail.save()
            
#             messages.success(request, "Task Updated Successfully ")
#             return redirect('update_task' , task_id )
#         print(task_form)
#         context = self.get_context_data(task_form=task_form, task_detail_form=task_detail_form)
#         return render(request,self.template_name,context)





@login_required
@permission_required('tasks.delete_task', login_url='no_permission')
def delete_task(request, id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=id)
        task.delete() 
        messages.success(request, f'Task "{task.title}" deleted successfully.')
    else:
        messages.error(request, "Invalid request method.")
    return redirect('manager_dashboard')



@login_required
@permission_required('tasks.view_task', login_url='no_permission')
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

view_task_decorators = [login_required, permission_required('projects.view_project', login_url='no_permission')]
@method_decorator(view_task_decorators, name='dispatch')
class ViewProject(ListView,View):
    model = Project
    context_object_name='projects'
    template_name = 'show_task.html'
    
    def get_queryset(self):
        queryset = Project.objects.annotate(num_task = Count('task')).order_by('num_task')
        
        return queryset


@login_required
@permission_required('tasks.view_task', login_url='no_permission')
def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    status_choices = Task.STATUS_CHOICES
    
    if request.method == "POST":
        selected_status = request.POST.get('task_status')
        # print(selected_status)
        task.status = selected_status
        task.save()
        messages.success(request, 'Task Status updated successfully.')
        return redirect('task_details', task.id)
    
    return render(request, 'task_details.html',{'task': task, 'status_choices': status_choices})


task_detail_decorators = [login_required, permission_required('tasks.view_task', login_url='no_permission')]
@method_decorator(task_detail_decorators, name='dispatch')
class TaskDetail(DetailView):
    model = Task
    template_name = 'task_details.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['status_choices']=Task.STATUS_CHOICES
        return context
    
    def post(self,request, *args, **kwargs):
        task = self.get_object()
        selected_status = request.POST.get('task_status')
        task.status = selected_status
        task.save()
        messages.success(request, 'Task Status updated successfully.')
        return redirect('task_details', task.id)


def dashboard(request):
    if is_employee(request.user):
        return redirect('user_dashboard')
    elif is_manager(request.user):
        return redirect('manager_dashboard')
    elif is_admin(request.user):
        return redirect('admin_dashboard')
    
    return redirect('no_permission')