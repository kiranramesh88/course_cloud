from django import forms
from instructor.models import User
from django.contrib.auth.forms import UserCreationForm

class StudentCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]    

def save(self, commit = True):
        user = super().save(commit=False)
        user.is_superuser=False
        user.is_staff=False
        user.is_active=True
        user.role="Student"
        if commit:
            user.save()

        return user

class StudentLoginForm(forms.Form):
     username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={"placeholder":"Enter Username","class":"form-control"}))
     password=forms.CharField(max_length=50,widget=forms.PasswordInput(attrs={"placeholder":"Enter Username","class":"form-control"}))
    
                             