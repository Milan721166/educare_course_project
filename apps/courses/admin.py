from django.contrib import admin
from .models import Course, CourseModule, StudentProgress

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'code', 'level', 'credits', 'is_active', 'created_by', 'enrolled_students_count']
    list_filter = ['level', 'is_active', 'created_at']
    list_editable = ['is_active']
    search_fields = ['title', 'code']

@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'duration_hours']
    list_filter = ['course']
    ordering = ['course', 'order']

@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ['student', 'module', 'is_completed', 'completed_at']
    list_filter = ['is_completed', 'completed_at']
    search_fields = ['student__username', 'module__title']