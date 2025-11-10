# from django.db import models
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class StudentProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     student_id = models.CharField(max_length=20, unique=True)
#     date_of_birth = models.DateField(null=True, blank=True)
#     address = models.TextField(blank=True)
#     enrollment_date = models.DateField(auto_now_add=True)
    
#     class Meta:
#         app_label = 'students'  # Add this line
    
#     def __str__(self):
#         return f"{self.user.username} - {self.student_id}"

# class Enrollment(models.Model):
#     STATUS_CHOICES = (
#         ('enrolled', 'Enrolled'),
#         ('in_progress', 'In Progress'),
#         ('completed', 'Completed'),
#         ('dropped', 'Dropped'),
#     )
    
#     student = models.ForeignKey(User, on_delete=models.CASCADE)
#     course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
#     enrollment_date = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
#     completion_date = models.DateTimeField(null=True, blank=True)
#     progress = models.IntegerField(default=0)  # 0-100 percentage
    
#     class Meta:
#         app_label = 'students'  # Add this line
#         unique_together = ['student', 'course']
    
#     def __str__(self):
#         return f"{self.student.username} - {self.course.title}"




from django.db import models
from django.contrib.auth import get_user_model

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
        ('enrolled', 'Enrolled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
    )
    
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    # Use string reference to avoid circular import
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
    completion_date = models.DateTimeField(null=True, blank=True)
    progress = models.IntegerField(default=0)
    
    class Meta:
        app_label = 'students'
        unique_together = ['student', 'course']
    
    def __str__(self):
        return f"{self.student.username} - {self.course.title}"