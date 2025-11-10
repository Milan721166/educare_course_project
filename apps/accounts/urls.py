from django.urls import path
from . import views

urlpatterns = [
    path('teacher/register/', views.teacher_register, name='teacher_register'),
    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('logout/', views.logout_view, name='logout'),
]