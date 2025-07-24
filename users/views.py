from django.shortcuts import render , redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.forms import RegisterForm,CustomRegistrationForm, LoginForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
# Create your views here.
def sign_up(request):
    
    form = CustomRegistrationForm()
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)    
            print('user', user)        
            user.is_active = False
            print(form.cleaned_data)
            user.set_password(form.cleaned_data['password'])
            user.save() 
            messages.success(request, 'A confirmation email sent. Check your email to activate your account.')
            return redirect('sign_in')
        else:
            print("Form are not valid")
    return render(request, 'registration/register.html', {"form" : form})

def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html', {'form': form })

def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign_in')
    
def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated successfully.')
            return redirect('sign_in')
        else:
            return HttpResponse('Invalid Id or Token')
            
    except User.DoesNotExist:
        return HttpResponse('User not found')