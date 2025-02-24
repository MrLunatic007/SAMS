from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.urls import reverse

def index(request):
    return render(request, 'Land.html')

def selection(request):
    return render(request, 'selection.html')

def student_login_user(request):
    # Redirect if user is already authenticated
    if request.user.is_authenticated and request.user.is_student:
        return redirect('core:student_dash')

    if request.method == "POST":
        # Getting the input - changed from 'login' to 'username' to match form field
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Login the user
                if user.is_student:
                    auth_login(request, user)
                    messages.success(request, f'Welcome back {username}!')
                    return redirect('core:student_dash')
                else:
                    messages.error(request, f'{user} role is not specified')
            else:
                messages.error(request, "Invalid username or password. Please try again.")
        else:
            messages.error(request, "Please provide both username and password.")
    
    return render(request, 'StudentLogin.html')

def teacher_login_user(request):
    # Redirect if user is already authenticated
    if request.user.is_authenticated and request.user.is_teacher:
        return redirect('core:teacher_dash')

    if request.method == "POST":
        # Getting the input - changed from 'login' to 'username' to match form field
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Login the user
                if user.is_teacher:
                    auth_login(request, user)
                    messages.success(request, f'Welcome back {username}!')
                    return redirect('core:teacher_dash')
                else:
                    messages.error(request, f'{user} role is not specified')
            else:
                messages.error(request, "Invalid username or password. Please try again.")
        else:
            messages.error(request, "Please provide both username and password.")
    
    return render(request, 'TeacherLogin.html')

def parent_login_user(request):
    # Redirect if user is already authenticated
    if request.user.is_authenticated and request.user.is_parent:
        return redirect('core:parent_dash')

    if request.method == "POST":
        # Getting the input - changed from 'login' to 'username' to match form field
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Login the user
                if user.is_parent:
                    auth_login(request, user)
                    messages.success(request, f'Welcome back {username}!')
                    return redirect('core:parent_dash')
                else:
                    messages.error(request, f'{user} role is not specified')
            else:
                messages.error(request, "Invalid username or password. Please try again.")
        else:
            messages.error(request, "Please provide both username and password.")
    
    return render(request, 'ParentLogin.html')

def user_logout(request):
    logout(request)
    return redirect('members:index')