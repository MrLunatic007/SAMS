from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'core'

urlpatterns =[

    ################################################################################
    ################################################################################
    ################################################################################
    ############################Student Urls########################################
    ################################################################################
    ################################################################################
    ################################################################################
    ################################################################################
    ################################################################################

    path('student/dashboard', views.studentdash, name="student_dash"),
    path("student/assignment", views.s_assignment, name="student_assignment"),
    path('student/assignment/download/<int:id>/', views.download, name='download'),

    ################################################################################
    ################################################################################
    ################################################################################
    ############################Teacher Urls########################################
    ################################################################################
    ################################################################################
    ################################################################################
    ################################################################################
    ################################################################################


    path('teacher/dashboard', views.teacherdash, name="teacher_dash"),
    path('teacher/assignments', views.t_assignments, name="teacher_assignments"),
    path('teacher/noticeboard', views.notice, name='notice'),
    path('teacher/assignments/delete/<int:id>', views.assign_delete, name='t_delete'), 
    path('teacher/noticeboard/delete/<int:id>', views.notice_delete, name='t_n_delete'), 


    # access denied urls
    path('access/denied', views.access_denied, name="access_denied"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)