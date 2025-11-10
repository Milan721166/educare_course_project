from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class TeacherRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'teacher'
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class TeacherLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)