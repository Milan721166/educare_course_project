# from django.urls import path
# from . import views

# urlpatterns = [
#     path('register/', views.student_register, name='student_register'),
#     path('login/', views.student_login, name='student_login'),
#     path('dashboard/', views.student_dashboard, name='student_dashboard'),
#     path('courses/', views.available_courses, name='student_courses'),
#     path('course/<int:course_id>/', views.course_detail, name='course_detail'),
#     path('module/<int:module_id>/complete/', views.update_module_progress, name='update_module_progress'),
#     path('profile/', views.student_profile, name='student_profile'),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.student_register, name='student_register'),
    path('login/', views.student_login, name='student_login'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('courses/', views.available_courses, name='student_courses'),
    path('profile/', views.student_profile, name='student_profile'),
    path('grades/', views.student_grades, name='student_grades'),
]