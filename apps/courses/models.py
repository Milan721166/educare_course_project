from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'courses'
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Course(models.Model):
    LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    )
    
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField()
    code = models.CharField(max_length=20, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    credits = models.IntegerField(default=3)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    duration_weeks = models.IntegerField(default=12)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True)
    video_intro = models.FileField(upload_to='course_intros/', blank=True)
    is_featured = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    requirements = models.TextField(blank=True)
    learning_outcomes = models.TextField(blank=True)
    
    class Meta:
        app_label = 'courses'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.code} - {self.title}"
    
    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'pk': self.pk})
    
    @property
    def current_price(self):
        return self.discount_price if self.discount_price else self.price
    
    @property
    def is_discounted(self):
        return self.discount_price is not None
    
    @property
    def discount_percentage(self):
        if self.is_discounted:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0
    
    @property
    def enrolled_students_count(self):
        # import using the full app path to ensure Django registers a single model class
        from apps.students.models import Enrollment
        return Enrollment.objects.filter(course=self, status__in=['enrolled', 'in_progress']).count()
    
    @property
    def total_modules(self):
        return self.modules.count()
    
    @property
    def total_duration(self):
        return sum(module.duration_hours for module in self.modules.all())

class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    duration_hours = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        app_label = 'courses'
        ordering = ['order']
        unique_together = ['course', 'order']
    
    def __str__(self):
        return f"{self.course.code} - Module {self.order}: {self.title}"

class Lesson(models.Model):
    LESSON_TYPES = (
        ('video', 'Video'),
        ('article', 'Article'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
    )
    
    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPES, default='article')
    video_url = models.URLField(blank=True)
    attachment = models.FileField(upload_to='lesson_attachments/', blank=True)
    order = models.IntegerField(default=0)
    duration_minutes = models.IntegerField(default=30)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        app_label = 'courses'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.module.course.code} - {self.title}"

class StudentProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        app_label = 'courses'
        unique_together = ['student', 'module']

    def __str__(self):
        return f"{self.student.username} - {self.module.title}"