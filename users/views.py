from django.shortcuts import render , redirect, HttpResponse
from django.contrib.auth.models import User , Group
from users.forms import CustomRegistrationForm, LoginForm , AssignRoleForm, CreateGroupForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
# Create your views here.

def is_admin(user):
    return user.groups.filter(name='Admin').exists()


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

@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
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
    
@user_passes_test(is_admin, login_url='no_permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
            Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
        ).all()
    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'
    return render(request, 'admin/dashboard.html', {'users': users})

@user_passes_test(is_admin, login_url='no_permission')
def assign_role(request, user_id):
    user = User.objects.get(id = user_id)
    form = AssignRoleForm()
    if request.method == 'POST': 
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear() # remove old role
            user.groups.add(role)
            messages.success(request,f'User {user.username} has been assigned to the {role.name} role')
            return redirect('admin_dashboard')
    
    return render(request, 'admin/assign_role.html',{'form': form})
            
@user_passes_test(is_admin, login_url='no_permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        print(form)
        if form.is_valid():
            group = form.save()
            messages.success(request,f'Group {group.name} has been created successfully')
            return redirect('create_group')
    return render(request, 'admin/create_group.html', {'form': form})

@user_passes_test(is_admin, login_url='no_permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})