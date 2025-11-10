from django.contrib import admin
from .models import StudentProfile, Enrollment

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'student_id', 'enrollment_date']
    list_filter = ['enrollment_date']
    search_fields = ['user__username', 'student_id']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'status', 'enrollment_date', 'progress']
    list_filter = ['status', 'enrollment_date']
    list_editable = ['status', 'progress']
    search_fields = ['student__username', 'course__title']