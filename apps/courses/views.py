from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Course, Category
from apps.students.models import Enrollment, Payment  # use full app path to avoid duplicate model registration

def course_list(request):
    """Display all published courses"""
    courses = Course.objects.filter(status='published').select_related('category')
    
    # Filtering
    category_id = request.GET.get('category')
    level = request.GET.get('level')
    search = request.GET.get('search')
    
    if category_id:
        courses = courses.filter(category_id=category_id)
    if level:
        courses = courses.filter(level=level)
    if search:
        courses = courses.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(code__icontains=search)
        )
    
    categories = Category.objects.all()
    
    context = {
        'courses': courses,
        'categories': categories,
        'selected_category': category_id,
        'selected_level': level,
        'search_query': search,
    }
    return render(request, 'courses/course_list.html', context)

def course_detail(request, pk):
    """Display course details"""
    course = get_object_or_404(Course, pk=pk, status='published')
    
    # Check if student is enrolled
    is_enrolled = False
    if request.user.is_authenticated and request.user.role == 'student':
        is_enrolled = Enrollment.objects.filter(
            student=request.user, 
            course=course,
            status__in=['enrolled', 'in_progress', 'completed']
        ).exists()
    
    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'modules': course.modules.filter(is_active=True),
    }
    return render(request, 'courses/course_detail.html', context)

@login_required
def enroll_course(request, pk):
    """Enroll student in a course"""
    if request.user.role != 'student':
        messages.error(request, 'Only students can enroll in courses.')
        return redirect('course_list')
    
    course = get_object_or_404(Course, pk=pk, status='published')
    
    # Check if already enrolled
    existing_enrollment = Enrollment.objects.filter(
        student=request.user, 
        course=course
    ).first()
    
    if existing_enrollment:
        if existing_enrollment.status in ['enrolled', 'in_progress']:
            messages.info(request, f'You are already enrolled in {course.title}.')
        elif existing_enrollment.status == 'completed':
            messages.info(request, f'You have already completed {course.title}.')
        else:
            existing_enrollment.status = 'enrolled'
            existing_enrollment.save()
            messages.success(request, f'Successfully enrolled in {course.title}!')
    else:
        # Create new enrollment
        enrollment = Enrollment.objects.create(
            student=request.user,
            course=course,
            status='enrolled'
        )
        
        # If course is free, create payment record
        if course.current_price == 0:
            Payment.objects.create(
                enrollment=enrollment,
                amount=0,
                status='completed'
            )
            messages.success(request, f'Successfully enrolled in {course.title}!')
        else:
            # For paid courses, redirect to payment page
            messages.info(request, f'Please complete payment for {course.title}.')
            # return redirect('payment_page', enrollment_id=enrollment.id)
            # For now, just enroll them
            messages.success(request, f'Successfully enrolled in {course.title}! (Payment simulation)')
    
    return redirect('student_dashboard')