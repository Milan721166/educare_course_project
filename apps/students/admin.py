from django.contrib import admin
from .models import StudentProfile, Enrollment, Payment

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'student_id', 'enrollment_date']
    list_filter = ['enrollment_date']
    search_fields = ['user__username', 'student_id']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'status', 'enrollment_date', 'progress', 'final_grade']
    list_filter = ['status', 'enrollment_date', 'certificate_issued']
    list_editable = ['status', 'progress']
    search_fields = ['student__username', 'course__title']
    readonly_fields = ['enrollment_date']
    
    actions = ['mark_as_completed', 'issue_certificates']
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} enrollments marked as completed.')
    mark_as_completed.short_description = "Mark selected enrollments as completed"
    
    def issue_certificates(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(status='completed').update(
            certificate_issued=True,
            certificate_issue_date=timezone.now()
        )
        self.message_user(request, f'{updated} certificates issued.')
    issue_certificates.short_description = "Issue certificates for completed courses"

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'amount', 'payment_date', 'status']
    list_filter = ['status', 'payment_date']
    list_editable = ['status']
    search_fields = ['enrollment__student__username', 'transaction_id']