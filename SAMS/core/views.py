from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .permissions import role_required
from members.models import StudentProfile, TeacherProfile, Subjects
from .models import Notice, Assignments, Exams

@login_required(login_url='members:login')
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
@login_required(login_url='members:login')
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
@login_required(login_url='members:login')
def s_assignment(request):
    return render(request, 'Students/assignments.html')

@role_required('is_student')
@login_required(login_url='members:login')  # Specify the login URL
def examdash(request):
    context ={
        'curret_page': 'exams'
    }
    return render(request, 'Students/exam.html', context)

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
@login_required(login_url='members:login')  # Specify the login URL
def teacherdash(request):
    try:
        teacher_profile = TeacherProfile.objects.get(user=request.user)
        subjects_taught = teacher_profile.subjects_taught.all()
        noticeb = Notice.objects.all()
    except TeacherProfile.DoesNotExist:
        teacher_profile = None
        subjects_taught = None

    context = {
        'user': request.user,
        'teacher_profile': teacher_profile,
        'subjects_taught': subjects_taught,
        'noticeb': noticeb,
    }
    return render(request, 'Teachers/dash.html', context)

@role_required('is_teacher')
@login_required(login_url='members:login')
def t_assignments(request):
    return render(request, 'Teachers/assignments.html')

@role_required('is_teacher')
@login_required(login_url='members:login')
def t_exams(request):
    if request.method == "POST":
        name = request.POST.get('title')
        start_date = request.POST.get('start_date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        description = request.POST.get('content')

        # Ensure you are using the correct model name
        new_exam = Exams(  # Adjusted to match your model name
            name=name,
            description=description,
            start_date=start_date,
            start_time=start_time,
            end_time=end_time,
        )
        new_exam.save()

    # Ensure `exams` is always defined, regardless of request method
    exams = Exams.objects.all()

    return render(request, 'Teachers/exam.html', {'exams': exams})

@role_required('is_teacher')
@login_required(login_url='members:login')
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
