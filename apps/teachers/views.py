from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

@login_required
def teacher_dashboard(request):
    if request.user.role != 'teacher' or not request.user.is_approved:
        messages.error(request, 'Access denied.')
        return redirect('home')
    return render(request, 'teachers/dashboard.html')

@staff_member_required
def admin_teacher_management(request):
    # Admin can manage teachers here
    from apps.accounts.models import User
    teachers = User.objects.filter(role='teacher')
    return render(request, 'teachers/admin_management.html', {'teachers': teachers})