from django.urls import path
from users.views import sign_up, activate_user
from users.views import ProfileView, CustomLogin, ChangePassword , CustomPasswordRestView, CustomPasswordRestConfirmView, EditProfileView
from users.views import CreateGroup,AssignRole, GroupList,AdminDashboard
from django.contrib.auth.views import  LogoutView, PasswordChangeView, PasswordChangeDoneView

urlpatterns = [
    path('sign_up/' , sign_up , name = "sign_up"),
    # path('sign_in/' , sign_in , name = "sign_in"),
    path('sign_in/' , CustomLogin.as_view() , name = "sign_in"),
    
    # path('sign_out/', sign_out, name='sign_out'),
    path('sign_out/', LogoutView.as_view(), name='logout'),
    path('activate/<int:user_id>/<str:token>/', activate_user, name = 'activate_user'),
    # path('admin/dashboard/', admin_dashboard, name = 'admin_dashboard'),
    path('admin/dashboard/', AdminDashboard.as_view(), name = 'admin_dashboard'),
    # path('admin/<int:user_id>/assign_role/', assign_role, name = 'assign_role'),
    path('admin/<int:user_id>/assign_role/', AssignRole.as_view(), name = 'assign_role'),
    # path('admin/create_group/', create_group, name = 'create_group'),
    path('admin/create_group/', CreateGroup.as_view(), name = 'create_group'),
    # path('admin/group_list/', group_list, name='group_list'),
    path('admin/group_list/', GroupList.as_view(), name='group_list'),
    path('profile/', ProfileView.as_view(template_name = 'accounts/profile.html'), name = 'profile'),
    path('profile/change_password/', ChangePassword.as_view(template_name='accounts/change_password.html'), name='change_password'),
    path('profile/change_password_done/',PasswordChangeDoneView.as_view(template_name='accounts/change_password_done.html'), name = 'password_change_done'),
    path('password_reset/', CustomPasswordRestView.as_view(), name='password_reset'),
    path('password_reset/confirm/<uidb64>/<token>/', CustomPasswordRestConfirmView.as_view(), name='password_reset_confirm'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    
]