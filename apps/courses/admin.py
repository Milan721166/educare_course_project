from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Course, CourseModule, Lesson

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ['name']}

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ['title', 'lesson_type', 'order', 'duration_minutes', 'is_active']

class CourseModuleInline(admin.TabularInline):
    model = CourseModule
    extra = 1
    fields = ['title', 'order', 'duration_hours', 'is_active']
    show_change_link = True

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'code', 'category', 'level', 'current_price', 
        'status', 'enrolled_students_count', 'is_featured', 'created_at'
    ]
    list_filter = ['status', 'level', 'category', 'is_featured', 'created_at']
    list_editable = ['status', 'is_featured']
    search_fields = ['title', 'code', 'description']
    readonly_fields = ['enrolled_students_count', 'total_modules', 'total_duration']
    filter_horizontal = []
    inlines = [CourseModuleInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'subtitle', 'code', 'category', 'description')
        }),
        ('Course Details', {
            'fields': ('level', 'credits', 'duration_weeks', 'requirements', 'learning_outcomes')
        }),
        ('Pricing', {
            'fields': ('price', 'discount_price', 'current_price', 'discount_percentage')
        }),
        ('Media', {
            'fields': ('thumbnail', 'video_intro')
        }),
        ('Status & Settings', {
            'fields': ('status', 'is_featured', 'created_by')
        }),
        ('Statistics', {
            'fields': ('enrolled_students_count', 'total_modules', 'total_duration'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'duration_hours', 'is_active']
    list_filter = ['course', 'is_active']
    list_editable = ['order', 'is_active']
    inlines = [LessonInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'lesson_type', 'order', 'duration_minutes', 'is_active']
    list_filter = ['lesson_type', 'is_active', 'module__course']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'module__title']