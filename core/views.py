from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .permissions import role_required
from members.models import StudentProfile, TeacherProfile, Subjects
from .models import Notice, Assignments
from django.http import FileResponse, Http404, HttpResponse
import os
from django.conf import settings
from wsgiref.util import FileWrapper
import datetime
from django.urls import reverse
from urllib.parse import quote
from docx2pdf import convert

@login_required(login_url='members:user_login')
def access_denied(request):
    return render(request, 'access.html', status=403)


################################################################################
################################################################################
################################################################################
############################Student Views#######################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################

@role_required('is_student')
@login_required(login_url='members:user_login')
def studentdash(request):
    try:
        student_profile = StudentProfile.objects.get(user=request.user)
        subjects = Subjects.objects.all()
        noticeb = Notice.objects.all()
    except StudentProfile.DoesNotExist or Subjects.DoesNotExist:
        student_profile = None  # Handle the case where the profile doesn't exist
        subjects = None
        noticeb = None

    context = {
        'user': request.user,
        'student_profile': student_profile,
        'subjects': subjects,
        'current_page': 'dashboard',
        'noticeb': noticeb
    }
    return render(request, 'Students/dash.html', context)

@role_required('is_student')
@login_required(login_url='members:user_login')
def s_assignment(request):
    assigns = Assignments.objects.all()
    return render(request, 'Students/assignments.html', {'assigns': assigns})


@role_required('is_student')
@login_required(login_url='members:user_login')  # Fixed typo in URL
def download(request, id):
    # Retrieve the assignment based on the given ID
    item = get_object_or_404(Assignments, id=id)
    
    # Check if the file exists
    if not item.file_name:
        raise Http404("File not found")
    
    # Get the file path
    file_path = os.path.join(settings.MEDIA_ROOT, str(item.file_name))
    
    # Verify the file exists and is within MEDIA_ROOT
    if not os.path.exists(file_path) or not os.path.commonpath([file_path, settings.MEDIA_ROOT]) == settings.MEDIA_ROOT:
        raise Http404("File not found")
    
    # Get the filename from the path
    filename = os.path.basename(file_path)
    
    try:
        # Open the file in binary mode
        file = open(file_path, 'rb')
        # Create the response with the file
        response = FileResponse(FileWrapper(file), content_type='application/force-download')
        # Set content disposition and filename
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except Exception as e:
        print(f"Error serving file: {e}")  # For debugging
        raise Http404("Error accessing file")


@role_required('is_student')
@login_required
def view_office_doc(request, assignment_id):
    try:
        assignment = get_object_or_404(Assignments, id=assignment_id)
        if not assignment.file_name:
            return HttpResponse("No file attached")
            
        file_url = request.build_absolute_uri(settings.MEDIA_URL + str(assignment.file_name))
        office_url = f'https://view.officeapps.live.com/op/embed.aspx?src={quote(file_url)}'
        
        print(f"File URL: {file_url}")  # Debug print
        print(f"Office URL: {office_url}")  # Debug print
        
        return render(request, 'Students/document_viewer.html', {
            'office_url': office_url,
            'assignment': assignment
        })
    except Exception as e:
        print(f"Error: {e}")  # Debug print
        return HttpResponse(f"Error viewing document: {e}")


################################################################################
################################################################################
################################################################################
############################Teacher Viwes#######################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################

@role_required('is_teacher')
@login_required(login_url='members:user_login')  # Specify the login URL
def teacherdash(request):
    try:
        teacher_profile = TeacherProfile.objects.get(user=request.user)
        subjects_taught = teacher_profile.subjects_taught.all()
        noticeb = Notice.objects.all()
    except TeacherProfile.DoesNotExist:
        teacher_profile = None
        subjects_taught = None
        noticeb = None  # Add this to avoid potential errors

    context = {
        'user': request.user,
        'teacher_profile': teacher_profile,
        'subjects_taught': subjects_taught,
        'noticeb': noticeb,
    }
    return render(request, 'Teachers/dash.html', context)

@role_required('is_teacher')
@login_required(login_url='members:user_login')
def t_assignments(request):
    current_date = datetime.datetime.now()
    if request.method == "POST":
        name = request.POST.get('title')
        due_date = request.POST.get('due_date')
        file = request.FILES.get('file')
        description = request.POST.get('description')
        createDate = current_date

        file = convert(file)

        new_assign = Assignments(
            name=name,
            description=description,
            due_date=due_date,
            file_name=file,
            createDate=createDate,
        )
        new_assign.save()
            
        return redirect('core:teacher_assignments')

    assigns = Assignments.objects.all()
    return render(request, 'Teachers/assignments.html', {'assigns': assigns, 'current_date': current_date})


@role_required('is_teacher')
@login_required(login_url='members:user_login')
def notice(request):
    if request.method == "POST":
        title = request.POST.get('title')
        importance = request.POST.get('importance')
        description = request.POST.get('content')  # Rename 'notice' to 'description' to match model field

        # Create and save a new Notice instance
        new_notice = Notice(
            name=title,
            importance=importance,
            description=description
        )
        new_notice.save()

        # Redirect to the same page or another after saving
        # return redirect('core:notice')  # Replace 'notice' with the name of your notice page route

    # If GET request, display existing notices
    noticeb = Notice.objects.all()
    return render(request, 'Teachers/notice.html', {'noticeb': noticeb})

@role_required('is_teacher')
@login_required(login_url='members:user_login')
def assign_delete(request, id):
    item = get_object_or_404(Assignments, id=id)
    item.delete()
    return redirect('core:teacher_assignments')

@role_required('is_teacher')
@login_required(login_url='members:user_login')
def notice_delete(request, id):
    item = get_object_or_404(Notice, id=id)
    item.delete()
    return redirect('core:notice')