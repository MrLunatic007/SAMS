from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .permissions import role_required
from members.models import StudentProfile, TeacherProfile, Subjects
from .models import Notice, Assignments
from django.http import FileResponse, Http404
import os

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
    except StudentProfile.DoesNotExist or Subjects.DoesNotExist:
        student_profile = None  # Handle the case where the profile doesn't exist
        subjects = None

    context = {
        'user': request.user,
        'student_profile': student_profile,
        'subjects': subjects,
        'current_page': 'dashboard',
    }
    return render(request, 'Students/dash.html', context)

@role_required('is_student')
@login_required(login_url='members:user_login')
def s_assignment(request):
    assigns = Assignments.objects.all()
    return render(request, 'Students/assignments.html', {'assigns': assigns})


@role_required('is_student')
@login_required(login_url='memebrs:user_login')
def download(request, id):
    # Retrieve the assignment based on the given ID
    item = get_object_or_404(Assignments, id=id)
    
    # Check if the file exists
    if not item.file_name:
        raise Http404("File not found.")
    
    # Get the path to the file in the media directory
    file_path = item.file_name.path  # This returns the full file path

    print(file_path)

    # Check if the file actually exists on the filesystem
    if not os.path.exists(file_path):
        raise Http404("File not found.")
    
    # Serve the file using FileResponse
    response = FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
    
    # Set the content-disposition header to trigger a download in the browser
    response['Content-Disposition'] = f'attachment; filename="{item.file_name.name}"'
    
    return response

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
    if request.method == "POST":
        name = request.POST.get('title')  # Corrected syntax
        due_date = request.POST.get('due_date')
        file = request.FILES.get('file')  # Handle file uploads using request.FILES
        description = request.POST.get('description')

        print(file)

        # Create and save the new assignment
        try: 
            new_assign = Assignments(
                name=name,
                description=description,
                due_date=due_date,
                file_name=file,  # Ensure this matches the field in the model
            )
            new_assign.save()
        except Exception as e:
            print("Error saving assignment:", e)


        print(new_assign.file_name)

        # Redirect to the same page to avoid duplicate submissions
        return redirect('core:teacher_assignments')  # Replace 't_assignments' with the actual URL name

    # Always fetch assignments for both POST and GET requests
    assigns = Assignments.objects.all()
    return render(request, 'Teachers/assignments.html', {'assigns': assigns})


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