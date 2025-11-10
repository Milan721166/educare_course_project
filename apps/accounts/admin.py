from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_approved', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_approved', 'is_staff', 'date_joined')
    list_editable = ('is_approved',)  # Allows direct editing from list view
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone', 'profile_picture', 'is_approved')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone', 'profile_picture', 'is_approved')
        }),
    )
    
    actions = ['approve_teachers', 'disapprove_teachers']
    
    def approve_teachers(self, request, queryset):
        # Only approve users with teacher role
        teachers = queryset.filter(role='teacher')
        updated = teachers.update(is_approved=True)
        self.message_user(request, f'{updated} teachers approved successfully.')
    approve_teachers.short_description = "Approve selected teachers"
    
    def disapprove_teachers(self, request, queryset):
        teachers = queryset.filter(role='teacher')
        updated = teachers.update(is_approved=False)
        self.message_user(request, f'{updated} teachers disapproved.')
    disapprove_teachers.short_description = "Disapprove selected teachers"

admin.site.register(User, CustomUserAdmin)