from django.urls import path
from tasks.views import manager_dashboard,test,user_dashboard,create_task,view_task,update_task,delete_task
urlpatterns = [
    path('manager_dashboard/',manager_dashboard,name = "manager_dashboard"),
    path('user_dashboard/',user_dashboard),
    path('test',test),
    path('create_task/',create_task, name =  'create_task'),
    path('view_task/',view_task),
    path('update_task/<int:id>/',update_task, name ="update_task"),
    path('delete_task/<int:id>/',delete_task, name ="delete_task"),
]

