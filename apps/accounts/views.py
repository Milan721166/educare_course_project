from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TeacherRegistrationForm, TeacherLoginForm
from .models import User

def teacher_register(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please wait for admin approval.')
            return redirect('teacher_login')
    else:
        form = TeacherRegistrationForm()
    return render(request, 'accounts/teacher_register.html', {'form': form})

def teacher_login(request):
    if request.method == 'POST':
        form = TeacherLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.role == 'teacher':
                if user.is_approved:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.username}!')
                    return redirect('teacher_dashboard')
                else:
                    messages.error(request, 'Your account is pending admin approval.')
            else:
                messages.error(request, 'Invalid credentials or account not approved.')
    else:
        form = TeacherLoginForm()
    return render(request, 'accounts/teacher_login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')