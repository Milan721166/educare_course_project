from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('admin/management/', views.admin_teacher_management, name='admin_teacher_management'),
]