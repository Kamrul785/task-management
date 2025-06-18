from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    # Http respons / json respons
    return HttpResponse("Welcome to the task management system")

def contact(request):
    return HttpResponse("This is contact page")

def show_task(request):
    return HttpResponse("<h1>This is our show_task page</h1>")

def show_specific_task(request,id):
    print("id",id)
    print("Id type",type(id))
    return HttpResponse(f"this is specific task page {id}")