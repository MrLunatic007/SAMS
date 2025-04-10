from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Shared Views
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('assignments/', views.assignments, name='assignments'),
    path('assignment/download/<int:id>/', views.download_assignment, name='download_assignment'),
    path('mark-notifications-as-read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),

    # Teacher Specific Views
    path('noticeboard/', views.notice_board, name='notice_board'),
    path('assignment/delete/<int:id>/', views.delete_assignment, name='delete_assignment'),
    path('noticeboard/delete/<int:id>/', views.delete_notice, name='delete_notice'),
    path('view/submissions/', views.view_submissions, name='view_submissions'),
    
    # Access Denied
    path('access-denied/', views.access_denied, name='access_denied'),
    
    # Legacy URLs for backward compatibility (redirects to consolidated views)
    path('student/dashboard/', views.dashboard, name='student_dash'),
    path('teacher/dashboard/', views.dashboard, name='teacher_dash'),
    path('parent/dashboard/', views.dashboard, name='parent_dash'),
    path('student/assignment/', views.assignments, name='student_assignment'),
    path('teacher/assignments/', views.assignments, name='teacher_assignments'),
    path('teacher/noticeboard/', views.notice_board, name='notice'),
    path('teacher/view/submissions/', views.view_submissions, name='t_v_submissions'),
    path('parent/student/progress', views.progress, name='progress')
]