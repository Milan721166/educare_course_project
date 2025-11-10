from django.db import models
from django.contrib.auth import get_user_model

from apps.courses.models import StudentProgress

User = get_user_model()

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    enrollment_date = models.DateField(auto_now_add=True)
    
    class Meta:
        app_label = 'students'
    
    def __str__(self):
        return f"{self.user.username} - {self.student_id}"

class Enrollment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Payment'),
        ('enrolled', 'Enrolled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('cancelled', 'Cancelled'),
    )
    
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    completion_date = models.DateTimeField(null=True, blank=True)
    progress = models.IntegerField(default=0)
    final_grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    certificate_issued = models.BooleanField(default=False)
    certificate_issue_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        app_label = 'students'
        unique_together = ['student', 'course']
    
    def __str__(self):
        return f"{self.student.username} - {self.course.title}"
    
    def update_progress(self):
        """Calculate progress based on completed lessons"""
        total_lessons = self.course.modules.aggregate(
            total=models.Sum('lessons__id', distinct=True)
        )['total'] or 0
        
        if total_lessons == 0:
            self.progress = 0
        else:
            completed_lessons = StudentProgress.objects.filter(
                student=self.student,
                lesson__module__course=self.course,
                is_completed=True
            ).count()
            self.progress = int((completed_lessons / total_lessons) * 100)
        
        self.save()

class Payment(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, default='credit_card')
    transaction_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    
    class Meta:
        app_label = 'students'
    
    def __str__(self):
        return f"Payment #{self.id} - {self.amount}"