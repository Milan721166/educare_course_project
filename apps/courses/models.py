# from django.db import models
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class Course(models.Model):
#     LEVEL_CHOICES = (
#         ('beginner', 'Beginner'),
#         ('intermediate', 'Intermediate'),
#         ('advanced', 'Advanced'),
#     )
    
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     code = models.CharField(max_length=20, unique=True)
#     credits = models.IntegerField(default=3)
#     level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
#     duration_weeks = models.IntegerField(default=12)
#     price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
#     is_active = models.BooleanField(default=True)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         app_label = 'courses'  # Add this line
    
#     def __str__(self):
#         return f"{self.code} - {self.title}"
    
#     @property
#     def enrolled_students_count(self):
#         return self.enrollment_set.filter(status__in=['enrolled', 'in_progress']).count()

# class CourseModule(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     title = models.CharField(max_length=200)
#     description = models.TextField(blank=True)
#     order = models.IntegerField(default=0)
#     duration_hours = models.IntegerField(default=1)
    
#     class Meta:
#         app_label = 'courses'  # Add this line
#         ordering = ['order']
    
#     def __str__(self):
#         return f"{self.course.code} - {self.title}"

# class StudentProgress(models.Model):
#     student = models.ForeignKey(User, on_delete=models.CASCADE)
#     module = models.ForeignKey(CourseModule, on_delete=models.CASCADE)
#     is_completed = models.BooleanField(default=False)
#     completed_at = models.DateTimeField(null=True, blank=True)
#     notes = models.TextField(blank=True)
    
#     class Meta:
#         app_label = 'courses'  # Add this line
#         unique_together = ['student', 'module']
    
#     def __str__(self):
#         return f"{self.student.username} - {self.module.title}"






from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Course(models.Model):
    LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    code = models.CharField(max_length=20, unique=True)
    credits = models.IntegerField(default=3)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    duration_weeks = models.IntegerField(default=12)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'courses'
    
    def __str__(self):
        return f"{self.code} - {self.title}"
    
    @property
    def enrolled_students_count(self):
        # Use string reference to avoid circular import
        from students.models import Enrollment
        return Enrollment.objects.filter(course=self, status__in=['enrolled', 'in_progress']).count()

class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    duration_hours = models.IntegerField(default=1)
    
    class Meta:
        app_label = 'courses'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.code} - {self.title}"

class StudentProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey('CourseModule', on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        app_label = 'courses'
        unique_together = ['student', 'module']
    
    def __str__(self):
        return f"{self.student.username} - {self.module.title}"