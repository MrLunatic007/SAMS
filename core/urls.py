from django.urls import path

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
    path('view-office/<int:assignment_id>/', views.view_assignment, name='view_office_doc'),


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
    path('teacher/submissions/', views.teacher_view_submissions, name='teacher_view_submissions'),


    # access denied urls
    path('access/denied', views.access_denied, name="access_denied"),
    # path('ckeditor/', include('ckeditor_uploader.urls')),
] 