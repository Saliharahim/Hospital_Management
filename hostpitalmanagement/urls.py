"""
URL configuration for hostpitalmanagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.SignUpView.as_view(),name="signup"),
    path('',views.SignInView.as_view(),name="signin"),
    path("password/change/",views.PasswordResetView.as_view(),name="password-reset"),
     path("create/timeslot/",views.CreateTimeSlotView.as_view(),name="addtime-slot"),
    path('index/',views.IndexView.as_view(),name="index"),
    path('doctor-add/',views.DoctorCreateView.as_view(),name="doctor-add"),
    path('department/create/',views.create_department, name='add-department'),
    path('department/list/',views.department_list, name='department-list'),
    path('department/edit/<int:department_id>/', views.edit_department, name='edit-department'),
    path('department/delete/<int:department_id>/', views.delete_department, name='delete-department'),
    path('create_appointment/', views.create_appointment, name='create_appointment'),

    path('appointment_confirmation/', views.send_confirmation_email, name='appointment_confirmation'),
    path('appointment_rejection/', views.send_rejection_email, name='appointment_rejection'),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
