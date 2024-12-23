from django.urls import path
from . import views

app_name = "members"

urlpatterns = [
    path('', views.login_user, name="user_login"),
    path('logout/', views.user_logout, name="user_logout")
]