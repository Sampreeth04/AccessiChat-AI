"""
URL configuration for disability_care project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from care_app import views
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from care_app.views import UserViewSet, PatientInfoViewSet, MedicationViewSet, AppointmentViewSet, ResponseGPT


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'gpt-response',ResponseGPT, basename = 'gpt-response')
router.register(r'patient-info', PatientInfoViewSet)
router.register(r'medications', MedicationViewSet)
router.register(r'appointments', AppointmentViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/openai/',ResponseGPT.as_view({'post':'response'}), name='openai_api'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('api/build-schedule/', views.build_schedule, name='build_schedule'),

    path('api/', include(router.urls)),

]
