from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import View,FormView
from myapp.forms import RegistrationForm,LoginForm,PasswordResetForm,DoctorForm,DepartmentForm,TimeSlotForm,AppointmentForm
from myapp.models import Doctor,Department,TimeSlot,Appointment,User
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from .decorators import signin_required, admin_required, superadmin_required
# Create your views here.

sadecks = [superadmin_required, signin_required, never_cache]
adecks = [admin_required, signin_required, never_cache]

decks = [signin_required, never_cache]


class SignUpView(View):
  
    model=User
    template_name="register.html"
    form_class=RegistrationForm
    def get(self,request,*args,**kwargs):
        form=self.form_class
        return render(request,self.template_name,{"form":form})
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"account has been created")
            return redirect("signin")
        messages.error(request,"failed to create account")
        return render(request,self.template_name,{"form":form})
class SignInView(View):
    model=User
    template_name="login.html"
    form_class=LoginForm
    def get(self,request,*args,**kwargs):
        form=self.form_class
        return render(request,self.template_name,{"form":form})
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"login success")
                return redirect("index")
            messages.error(request,"login error")
            return render(request,self.template_name,{"form":form})
class PasswordResetView(FormView):
    model=User
    template_name="password-reset.html"
    form_class=PasswordResetForm
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            email=form.cleaned_data.get("email")
            pwd1=form.cleaned_data.get("password1")
            pwd2=form.cleaned_data.get("password2")
            if pwd1==pwd2:
                try:
                    usr=User.objects.get(username=username,email=email)
                    
                    usr.set_password(pwd1)
                    usr.save()
                    messages.success(request,"password changed")
                    return redirect("signin")
                except Exception as e:
                    messages.error(request,"invalid ctredentials")
                    return render(request,self.template_name,{"form":form})
            else:
                messages.error(request,"password mismatch")
                return render(request,self.template_name,{"form":form})
    
@method_decorator(adecks, name='dispatch')
class DoctorCreateView(View):
    model=Doctor
    form_class=DoctorForm
    template_name="doctor-add.html"
    def get(self,request,*args,**kwargs):
        form=self.form_class
        return render(request,self.template_name,{"form":form})
    def post(self,request,*args,**kwargs):
        form=self.form_class(files=request.FILES,data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"create doctor successfully")
            return redirect("doctor-add")
        messages.error(request,"failed to create doctor")
        return render(request,self.template_name,{"form":form})
@method_decorator(decks, name='dispatch')
class IndexView(View):
    template_name="index.html"
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)
# @method_decorator(sadecks, name='dispatch')
def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department-list')
    else:
        form = DepartmentForm()
    return render(request, 'add-department.html', {'form': form})
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department-list.html', {'departments': departments})

def edit_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('department-list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'edit-department.html', {'form': form})

def delete_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    if request.method == 'POST':
        department.delete()
        return redirect('department-list')
    return render(request, 'delete-department.html', {'department': department})


def send_confirmation_email(appointment):
    subject = 'Appointment Confirmation'
    message = f'Your appointment on {appointment.date} at {appointment.time_slot} with Dr. {appointment.doctor} has been confirmed.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [appointment.email]
    
    # Use the send_mail function to send the confirmation email
    send_mail(subject, message, from_email, recipient_list)

def send_rejection_email(appointment):
    subject = 'Appointment Rejection'
    message = f'Sorry, the requested time slot for the appointment with Dr. {appointment.doctor} is not available.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [appointment.email]
    
    
    send_mail(subject, message, from_email, recipient_list)

def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            
          
            doctor = appointment.doctor
            selected_time_slot = appointment.time_slot
            
            if doctor.is_available(selected_time_slot.start_time):
                appointment.save()
                send_confirmation_email(appointment)
                return redirect('appointment_confirmation')
            else:
                send_rejection_email(appointment)
                return redirect('appointment_rejection')

    else:
        form = AppointmentForm()
    return render(request, 'appointment_form.html', {'form': form})
@method_decorator(adecks, name='dispatch')
class CreateTimeSlotView(View):
    template_name = 'addtime-slot.html'

    def get(self, request):
        form = TimeSlotForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TimeSlotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('addtime-slot')  
        return render(request, self.template_name, {'form': form})