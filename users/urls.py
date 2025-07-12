from django.urls import path
from users.views import sign_up
urlpatterns = [
    path('sign_up/' , sign_up , name = "sign_up")
]