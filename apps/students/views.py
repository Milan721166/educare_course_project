# # from django.shortcuts import render, redirect, get_object_or_404
# # from django.contrib.auth import login, authenticate, logout
# # from django.contrib.auth.decorators import login_required
# # from django.contrib import messages
# # from django.db.models import Count, Q
# # from .forms import StudentRegistrationForm, StudentLoginForm, CourseEnrollmentForm
# # from .models import Enrollment, StudentProfile
# # from apps.courses.models import Course, CourseModule, StudentProgress

# # def student_register(request):
# #     if request.method == 'POST':
# #         form = StudentRegistrationForm(request.POST)
# #         if form.is_valid():
# #             user = form.save()
# #             messages.success(request, 'Registration successful! You can now login.')
# #             return redirect('student_login')
# #     else:
# #         form = StudentRegistrationForm()
# #     return render(request, 'students/register.html', {'form': form})

# # def student_login(request):
# #     if request.method == 'POST':
# #         form = StudentLoginForm(request.POST)
# #         if form.is_valid():
# #             username = form.cleaned_data['username']
# #             password = form.cleaned_data['password']
# #             user = authenticate(request, username=username, password=password)
# #             if user is not None and user.role == 'student':
# #                 login(request, user)
# #                 messages.success(request, f'Welcome back, {user.username}!')
# #                 return redirect('student_dashboard')
# #             else:
# #                 messages.error(request, 'Invalid credentials or not a student account.')
# #     else:
# #         form = StudentLoginForm()
# #     return render(request, 'students/login.html', {'form': form})

# # @login_required
# # def student_dashboard(request):
# #     if request.user.role != 'student':
# #         messages.error(request, 'Access denied.')
# #         return redirect('home')
    
# #     # Get student enrollments
# #     enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    
# #     # Statistics
# #     total_courses = enrollments.count()
# #     completed_courses = enrollments.filter(status='completed').count()
# #     in_progress_courses = enrollments.filter(status='in_progress').count()
    
# #     context = {
# #         'enrollments': enrollments,
# #         'total_courses': total_courses,
# #         'completed_courses': completed_courses,
# #         'in_progress_courses': in_progress_courses,
# #     }
# #     return render(request, 'students/dashboard.html', context)

# # @login_required
# # def available_courses(request):
# #     if request.user.role != 'student':
# #         messages.error(request, 'Access denied.')
# #         return redirect('home')
    
# #     # Get courses not enrolled by student
# #     enrolled_course_ids = Enrollment.objects.filter(student=request.user).values_list('course_id', flat=True)
# #     available_courses = Course.objects.filter(is_active=True).exclude(id__in=enrolled_course_ids)
    
# #     # Enrollment form
# #     if request.method == 'POST':
# #         form = CourseEnrollmentForm(request.POST)
# #         if form.is_valid():
# #             course = form.cleaned_data['course']
# #             # Check if already enrolled
# #             if not Enrollment.objects.filter(student=request.user, course=course).exists():
# #                 Enrollment.objects.create(student=request.user, course=course)
# #                 messages.success(request, f'Successfully enrolled in {course.title}')
# #             else:
# #                 messages.warning(request, f'You are already enrolled in {course.title}')
# #             return redirect('student_courses')
# #     else:
# #         form = CourseEnrollmentForm()
    
# #     context = {
# #         'available_courses': available_courses,
# #         'form': form,
# #     }
# #     return render(request, 'students/available_courses.html', context)

# # @login_required
# # def course_detail(request, course_id):
# #     if request.user.role != 'student':
# #         messages.error(request, 'Access denied.')
# #         return redirect('home')
    
# #     course = get_object_or_404(Course, id=course_id)
# #     enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
# #     modules = CourseModule.objects.filter(course=course)
    
# #     # Get progress for each module
# #     module_progress = []
# #     for module in modules:
# #         progress, created = StudentProgress.objects.get_or_create(
# #             student=request.user,
# #             module=module
# #         )
# #         module_progress.append({
# #             'module': module,
# #             'progress': progress
# #         })
    
# #     # Calculate overall course progress
# #     total_modules = modules.count()
# #     completed_modules = StudentProgress.objects.filter(
# #         student=request.user,
# #         module__course=course,
# #         is_completed=True
# #     ).count()
    
# #     overall_progress = (completed_modules / total_modules * 100) if total_modules > 0 else 0
    
# #     context = {
# #         'course': course,
# #         'enrollment': enrollment,
# #         'module_progress': module_progress,
# #         'overall_progress': overall_progress,
# #         'completed_modules': completed_modules,
# #         'total_modules': total_modules,
# #     }
# #     return render(request, 'students/course_detail.html', context)

# # @login_required
# # def update_module_progress(request, module_id):
# #     if request.user.role != 'student':
# #         messages.error(request, 'Access denied.')
# #         return redirect('home')
    
# #     module = get_object_or_404(CourseModule, id=module_id)
# #     progress, created = StudentProgress.objects.get_or_create(
# #         student=request.user,
# #         module=module
# #     )
    
# #     if not progress.is_completed:
# #         progress.is_completed = True
# #         progress.save()
# #         messages.success(request, f'Marked {module.title} as completed!')
# #     else:
# #         messages.info(request, f'{module.title} was already completed.')
    
# #     return redirect('course_detail', course_id=module.course.id)

# # @login_required
# # def student_profile(request):
# #     if request.user.role != 'student':
# #         messages.error(request, 'Access denied.')
# #         return redirect('home')
    
# #     profile = get_object_or_404(StudentProfile, user=request.user)
# #     enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    
# #     context = {
# #         'profile': profile,
# #         'enrollments': enrollments,
# #     }
# #     return render(request, 'students/profile.html', context)











# from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .forms import StudentRegistrationForm, StudentLoginForm

# def student_register(request):
#     if request.method == 'POST':
#         form = StudentRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             messages.success(request, 'Registration successful! You can now login.')
#             return redirect('student_login')
#     else:
#         form = StudentRegistrationForm()
#     return render(request, 'students/register.html', {'form': form})

# def student_login(request):
#     if request.method == 'POST':
#         form = StudentLoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None and user.role == 'student':
#                 login(request, user)
#                 messages.success(request, f'Welcome back, {user.username}!')
#                 return redirect('student_dashboard')
#             else:
#                 messages.error(request, 'Invalid credentials or not a student account.')
#     else:
#         form = StudentLoginForm()
#     return render(request, 'students/login.html', {'form': form})

# @login_required
# def student_dashboard(request):
#     if request.user.role != 'student':
#         messages.error(request, 'Access denied.')
#         return redirect('home')
    
#     context = {
#         'total_courses': 0,
#         'completed_courses': 0,
#         'in_progress_courses': 0,
#     }
#     return render(request, 'students/dashboard.html', context)









from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegistrationForm, StudentLoginForm, CourseEnrollmentForm
from .models import Enrollment, StudentProfile

def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! You can now login.')
            return redirect('student_login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'students/register.html', {'form': form})

def student_login(request):
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.role == 'student':
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('student_dashboard')
            else:
                messages.error(request, 'Invalid credentials or not a student account.')
    else:
        form = StudentLoginForm()
    return render(request, 'students/login.html', {'form': form})

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    enrollments = Enrollment.objects.filter(student=request.user)
    
    total_courses = enrollments.count()
    completed_courses = enrollments.filter(status='completed').count()
    in_progress_courses = enrollments.filter(status='in_progress').count()
    
    context = {
        'enrollments': enrollments,
        'total_courses': total_courses,
        'completed_courses': completed_courses,
        'in_progress_courses': in_progress_courses,
    }
    return render(request, 'students/dashboard.html', context)

@login_required
def student_profile(request):
    """View for student profile"""
    if request.user.role != 'student':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        # Create profile if it doesn't exist
        profile = StudentProfile.objects.create(user=request.user, student_id=f"STU{request.user.id:04d}")
    
    enrollments = Enrollment.objects.filter(student=request.user)
    
    context = {
        'profile': profile,
        'enrollments': enrollments,
    }
    return render(request, 'students/profile.html', context)

@login_required
def available_courses(request):
    """View for students to browse available courses"""
    if request.user.role != 'student':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Simple course data (we'll replace this with database later)
    sample_courses = [
        {'title': 'Introduction to Programming', 'level': 'Beginner', 'description': 'Learn basic programming concepts'},
        {'title': 'Web Development', 'level': 'Intermediate', 'description': 'Build modern web applications'},
        {'title': 'Data Science', 'level': 'Advanced', 'description': 'Analyze and visualize data'},
        {'title': 'Database Management', 'level': 'Intermediate', 'description': 'Learn SQL and database design'},
        {'title': 'Mobile App Development', 'level': 'Advanced', 'description': 'Build cross-platform mobile apps'},
        {'title': 'Cyber Security', 'level': 'Advanced', 'description': 'Learn security best practices'},
    ]
    
    context = {
        'courses': sample_courses
    }
    return render(request, 'students/available_courses.html', context)

@login_required
def student_grades(request):
    """View for student grades (placeholder)"""
    if request.user.role != 'student':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    context = {
        'message': 'Grade tracking feature coming soon!'
    }
    return render(request, 'students/grades.html', context)