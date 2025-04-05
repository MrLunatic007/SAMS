from django.urls import path
from . import views

app_name = "members"

urlpatterns = [
    path('', views.index, name='index'),
    path('selection/', views.selection, name="userSelection"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.user_logout, name="user_logout"),
    path('CommingSoon/', views.CommingSoon, name='CommingSoon'),
]