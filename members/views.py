from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.urls import reverse

from core.models import Notice

def index(request):
    try:
        noticeb = Notice.objects.all()
    except Notice.DoesNotExist:
        noticeb = None

    context = {
        'noticeb': noticeb
    }

    return render(request, 'Land.html', context)

def selection(request):
    return render(request, 'selection.html')

def apply(request):
    return render(request, 'apply.html')

def login_user(request):
    # Get user type from GET parameter or POST data
    user_type = request.POST.get('user_type') or request.GET.get('user_type', 'student')
    
    # Validate that user_type is one of the acceptable values
    if user_type not in ['student', 'teacher', 'parent']:
        user_type = 'student'  # Default to student if invalid
    
    # Check if the user is already authenticated with the correct role
    if request.user.is_authenticated:
        if (user_type == 'student' and request.user.is_student) or \
           (user_type == 'teacher' and request.user.is_teacher) or \
           (user_type == 'parent' and request.user.is_parent):
            return redirect(f'core:{user_type}_dash')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Check if user has the required role
                if (user_type == 'student' and user.is_student) or \
                   (user_type == 'teacher' and user.is_teacher) or \
                   (user_type == 'parent' and user.is_parent):
                    auth_login(request, user)
                    messages.success(request, f'Welcome back {username}!')
                    return redirect(f'core:{user_type}_dash')
                else:
                    messages.error(request, f'Your account does not have {user_type} privileges')
            else:
                messages.error(request, "Invalid username or password. Please try again.")
        else:
            messages.error(request, "Please provide both username and password.")
    
    context = {
        'user_type': user_type
    }
    
    return render(request, 'Login.html', context)

def user_logout(request):
    logout(request)
    return redirect('members:index')

def CommingSoon(request):
    return render(request, 'CommingSoon.html')