from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .permissions import role_required
from members.models import StudentProfile, TeacherProfile, Subjects, ParentProfile
from .models import Notice, Assignments, AssignmentSubmission
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
import os
from django.conf import settings
from wsgiref.util import FileWrapper
from datetime import datetime
from django.urls import reverse
from urllib.parse import quote
from django.contrib import messages
from django.utils import timezone


@login_required(login_url='members:userSelection')
def access_denied(request):
    return render(request, 'UI/access.html', status=403)

@login_required(login_url='members:index')
def profile(request):
    context = {}
    try:
        if request.user.is_student:
            profile_instance = StudentProfile.objects.get(user=request.user)
            context['student_profile'] = profile_instance
        elif request.user.is_teacher:
            profile_instance = TeacherProfile.objects.get(user=request.user)
            context['teacher_profile'] = profile_instance
        elif request.user.is_parent:
            profile_instance = ParentProfile.objects.get(user=request.user)
            context['parent_profile'] = profile_instance
            context['students_profile'] = profile_instance.student
    except (StudentProfile.DoesNotExist, TeacherProfile.DoesNotExist, ParentProfile.DoesNotExist):
        messages.error(request, "Profile not found.")
        return redirect('members:index')

    return render(request, 'UI/profile.html', context)

def notification_processor(request):
    """
    Context processor to add notification count to all templates.
    """
    if request.user.is_authenticated:
        try:
            notification_count = Notice.objects.count()
        except:
            notification_count = 0
        
        return {
            'notification_count': notification_count
        }
    return {'notification_count': 0}

@login_required
def mark_notifications_as_read(request):
    """
    Mark all notifications as read for the current user.
    """
    try:
        # Get all unread notices
        notices = Notice.objects.all()
        
        # Mark them as read by adding the current user to read_by
        for notice in notices:
            notice.read_by.add(request.user)
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def get_notification_count(request):
    """
    Returns the count of unread notifications for the current user.
    """
    try:
        notification_count = Notice.objects.count()
        return notification_count
    except:
        return 0

################################################################################
# Consolidated Dashboard View
################################################################################
@login_required
def dashboard(request):
    context = {
        'user': request.user,
        'noticeb': Notice.objects.all()
    }
    
    try:
        if request.user.is_student:
            student_profile = StudentProfile.objects.get(user=request.user)
            context['student_profile'] = student_profile
            context['study_profile'] = student_profile.subjects.all()
            
        elif request.user.is_teacher:
            teacher_profile = TeacherProfile.objects.get(user=request.user)
            context['teacher_profile'] = teacher_profile
            context['subjects_taught'] = teacher_profile.subjects_taught.all()
            
        elif request.user.is_parent:
            parent_profile = ParentProfile.objects.get(user=request.user)
            context['parent_profile'] = parent_profile
            
            # Get related student profiles
            students_profile = StudentProfile.objects.filter(id__in=parent_profile.students.all())
            context['students_profile'] = students_profile
            
            # If viewing a specific student, add their subjects to context
            if 'student_id' in request.GET:
                try:
                    student = students_profile.get(student_id=request.GET['student_id'])
                    context['study_profile'] = student.subjects.all()
                except StudentProfile.DoesNotExist:
                    pass
    except (StudentProfile.DoesNotExist, TeacherProfile.DoesNotExist, ParentProfile.DoesNotExist):
        messages.error(request, "Profile not found.")
    
    return render(request, 'UI/dashboard.html', context)

################################################################################
# Consolidated Assignment Views
################################################################################
@login_required
def assignments(request):
    context = {
        'user': request.user,
        'assigns': Assignments.objects.all(),
        'current_date': datetime.now()
    }
    
    if request.user.is_student:
        # Student assignments view with submissions
        submissions = {
            sub.assignment_id: sub 
            for sub in AssignmentSubmission.objects.filter(student__user=request.user)
        }
        context['submissions'] = submissions
        
    elif request.user.is_teacher and request.method == "POST":
        # Teacher assignment creation
        name = request.POST.get('title')
        due_date = request.POST.get('due_date')
        file = request.FILES.get('file')
        description = request.POST.get('description')
        
        new_assign = Assignments(
            name=name,
            description=description,
            due_date=due_date,
            file_name=file,
            createDate=datetime.now(),
        )
        new_assign.save()
        return redirect('core:assignments')
    
    return render(request, 'UI/assignment.html', context)

@login_required
def download_assignment(request, id):
    item = get_object_or_404(Assignments, id=id)
    
    if not item.file_name:
        raise Http404("File not found")
    
    file_path = os.path.join(settings.MEDIA_ROOT, str(item.file_name))
    
    if not os.path.exists(file_path) or not os.path.commonpath([file_path, settings.MEDIA_ROOT]) == settings.MEDIA_ROOT:
        raise Http404("File not found")
    
    filename = os.path.basename(file_path)
    
    try:
        file = open(file_path, 'rb')
        response = FileResponse(FileWrapper(file), content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except Exception as e:
        print(f"Error serving file: {e}")
        raise Http404("Error accessing file")

@login_required
def delete_assignment(request, id):
    if not request.user.is_teacher:
        return redirect('core:access_denied')
        
    item = get_object_or_404(Assignments, id=id)
    item.delete()
    return redirect('core:assignments')

################################################################################
# Notice Views
################################################################################
@login_required
def notice_board(request):
    if request.user.is_teacher and request.method == "POST":
        title = request.POST.get('title')
        importance = request.POST.get('importance')
        description = request.POST.get('content')

        new_notice = Notice(
            name=title,
            importance=importance,
            description=description
        )
        new_notice.save()

    noticeb = Notice.objects.all()
    return render(request, 'UI/notice.html', {'noticeb': noticeb})

@login_required
def delete_notice(request, id):
    if not request.user.is_teacher:
        return redirect('core:access_denied')
        
    item = get_object_or_404(Notice, id=id)
    item.delete()
    return redirect('core:notice_board')

################################################################################
# Teacher Submission Views
################################################################################
@login_required
def view_submissions(request):
    if not request.user.is_teacher:
        return redirect('core:access_denied')
        
    submissions = AssignmentSubmission.objects.select_related('student', 'assignment').filter(status='submitted').order_by('-submitted_at')
    
    # Get all students who haven't submitted assignments
    all_assignments = Assignments.objects.all()
    all_students = StudentProfile.objects.all()
    
    # Create a dictionary of non-submissions
    non_submissions = []
    
    for assignment in all_assignments:
        for student in all_students:
            # Check if this student has submitted this assignment
            if not AssignmentSubmission.objects.filter(
                student=student, 
                assignment=assignment
            ).exists():
                non_submissions.append({
                    'student': student,
                    'assignment': assignment
                })
    
    return render(request, 'UI/view_submissions.html', {
        'submissions': submissions,
        'non_submissions': non_submissions
    })