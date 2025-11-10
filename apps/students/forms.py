# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from apps.accounts.models import User
# # from .models import StudentProfile  # Comment this out temporarily

# class StudentRegistrationForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     phone = forms.CharField(max_length=15, required=False)
#     student_id = forms.CharField(max_length=20, required=True)
    
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'phone', 'student_id', 'password1', 'password2']
    
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.role = 'student'
#         user.email = self.cleaned_data['email']
        
#         if commit:
#             user.save()
#             # We'll add profile creation later
#         return user

# class StudentLoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

# class CourseEnrollmentForm(forms.Form):
#     course = forms.ModelChoiceField(queryset=None, empty_label="Select a course")
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # We'll add the queryset later
#         pass





from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.accounts.models import User
from .models import StudentProfile

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)
    student_id = forms.CharField(max_length=20, required=True)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'student_id', 'date_of_birth', 'address', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                student_id=self.cleaned_data['student_id'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                address=self.cleaned_data['address']
            )
        return user

class StudentLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class CourseEnrollmentForm(forms.Form):
    course = forms.ModelChoiceField(queryset=None, empty_label="Select a course")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Import inside method to avoid circular import
        from apps.courses.models import Course
        self.fields['course'].queryset = Course.objects.filter(is_active=True)