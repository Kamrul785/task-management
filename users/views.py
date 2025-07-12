from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.forms import RegisterForm
# Create your views here.
def sign_up(request):
    
    if request.method == "GET":
        form = RegisterForm()
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password1')
            # confirm_password =  form.cleaned_data.get('password2')
            # if password == confirm_password:
            #     User.objects.Create(username = username, password = password)
            # else:
            #     print('password are not same')
            form.save()                
        else:
            print("Form are not valid")
            
    return render(request, 'registration/register.html', {"form" : form})