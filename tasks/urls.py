from django.urls import path
from tasks.views import manager_dashboard,employee_dashboard,create_task,view_task,task_detail,update_task,delete_task,dashboard
from tasks.views import Greetings,HiGreetings, CreateTask,UpdateTask,ViewProject,TaskDetail,EmployeeDashboardView

urlpatterns = [
    path('manager_dashboard/',manager_dashboard,name = "manager_dashboard"),
    # path('employee_dashboard/',employee_dashboard, name = 'user_dashboard'),
    path('employee_dashboard/',EmployeeDashboardView.as_view(), name = 'user_dashboard'),
    # path('create_task/',create_task, name =  'create_task'),
    path('create_task/',CreateTask.as_view(), name =  'create_task'),
    # path('view_task/',view_task, name='view_task'),
    path('view_task/',ViewProject.as_view(), name='view_task'),
    # path('task/<int:task_id>/details/',task_detail, name = 'task_details'),
    path('task/<int:task_id>/details/',TaskDetail.as_view(), name = 'task_details'),
    # path('update_task/<int:id>/',update_task, name ="update_task"),
    path('update_task/<int:id>/',UpdateTask.as_view(), name ="update_task"),
    path('delete_task/<int:id>/',delete_task, name ="delete_task"),
    path('dashboard/', dashboard, name = 'dashboard'),
    
    
    #CBV PATHS
    path('greetings/', Greetings.as_view(), name = 'greetings'),
    path('higreetings/', HiGreetings.as_view(), name = 'higreetings'),
]

