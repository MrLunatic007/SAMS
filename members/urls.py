from django.urls import path
from . import views

app_name = "members"

urlpatterns = [
    path('', views.index, name='index'),
    path('selection/', views.selection, name="userSelection"),
    path('teacher/', views.teacher_login_user, name="teacher_user_login"),
    path('student/', views.student_login_user, name="student_user_login"),
    path('parent/', views.parent_login_user, name='parent_user_login'),
    path('logout/', views.user_logout, name="user_logout"),
    path('CommingSoon/', views.CommingSoon, name='CommingSoon'),
]