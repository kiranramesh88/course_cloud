from django import forms
from instructor.models import User
from django.contrib.auth.forms import UserCreationForm


class InstructorForm(UserCreationForm):
    class Meta:
        model=User
        fields=["first_name","email","username","password1","password2"]
        widgets={
            "first_name": forms.TextInput(attrs={"placeholder": "enter first name","class": "form-control"}),
            "email": forms.TextInput(attrs={"placeholder": "enter email","class": "form-control"}),
            "username": forms.TextInput(attrs={"placeholder": "enter username","class": "form-control"}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].widget.attrs.update({
            "placeholder": "enter password",
            "class": "form-control"
        })

        self.fields["password2"].widget.attrs.update({
            "placeholder": "re-enter password",
            "class": "form-control"
        })


    def save(self, commit = True):
        user = super().save(commit=False)
        user.is_superuser=True
        user.is_staff=True
        user.is_active=True
        user.role="Instrucor"
        if commit:
            user.save()

        return user
