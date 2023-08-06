# from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from myapp.models import Doctor,Department,Appointment,TimeSlot,User

class RegistrationForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    class Meta:
        model=User
        fields=["username","email","password1","password2"]
        widgets={
             "username":forms.TextInput(attrs={"class":"form-control"}),
            
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            }
class LoginForm(forms.Form):
    
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
class PasswordResetForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control"}))
    password1=forms.CharField(label="new password", widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(label="confirm new password", widget=forms.PasswordInput(attrs={"class":"form-control"}))
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            "photo": forms.FileInput(attrs={"class": "form-control"}),
            "qualification": forms.TextInput(attrs={"class": "form-control"}),
        }
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"})

         }
class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['start_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'class': 'form-control'}),
            # 'end_time': forms.TimeInput(attrs={'class': 'form-control'}),
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = "__all__"
        
