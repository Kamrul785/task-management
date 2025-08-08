from django import forms
import re
from django.contrib.auth.forms import UserCreationForm , PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import Group, Permission
from tasks.forms import StyledFormMixin
from django.contrib.auth.forms import AuthenticationForm
from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username' , 'first_name', 'last_name', 'password1', 'password2' , 'email'] 
    
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            
class CustomRegistrationForm(StyledFormMixin,forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User 
        fields = ['username', 'first_name', 'last_name' , 'password','confirm_password', 'email']
        
    def clean_password(self):
        password = self.cleaned_data.get('password')
        error = []
        if len(password) < 8:
            error.append('Password must be at least 8 character long')
        
        if not re.search(r'[A-Z]', password):
            error.append('Password must include at least one uppercase letter')
        
        if not re.search(r'[a-z]', password):
            error.append('Password must include at least one lowercaser latter')
        
        if not re.search(r'[0-9]', password):
            error.append('Password must include at least one number')
         
        if not re.search(r'[!@#$%^&*(){}]', password):
            error.append('Password must include at one specail character')
        
        if error : 
            raise forms.ValidationError(error)
        
        return password
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exits = User.objects.filter(email = email).exists()
        if email_exits:
            raise forms.ValidationError("Email Already Exits")
        return email 
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password :
            raise forms.ValidationError("Password do not match")
        return cleaned_data

        
class LoginForm(StyledFormMixin,AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
class AssignRoleForm(StyledFormMixin,forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label = 'Select a role'
    )
    
class CreateGroupForm(StyledFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label = 'Assign Permissions'
    )
    
    class Meta:
        model = Group
        fields = ['name', 'permissions']
    
    
class CustomPasswordChangeForm(StyledFormMixin, PasswordChangeForm):
    pass

class CustomPasswordRestForm(StyledFormMixin, PasswordResetForm):
    pass

class CustomPasswordRestConfirmForm(StyledFormMixin, SetPasswordForm):
    pass

class EditProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'profile_image', 'bio']
        
        