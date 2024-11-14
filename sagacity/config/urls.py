"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
# config/urls.py
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from sagacity.dashboard import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('assignment/<int:pk>/', views.assignment_detail, name='assignment_detail'),
    path('my-assignments/', views.my_assignments, name='my_assignments'),
    path('create-assignment/', views.create_assignment, name='create_assignment'),
    path('edit-assignment/<int:pk>/', views.edit_assignment, name='edit_assignment'),
    path('delete-assignment/<int:pk>/', views.delete_assignment, name='delete_assignment'),
    path('toggle-assignment/<int:pk>/', views.toggle_assignment, name='toggle_assignment'),
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='dashboard/password_reset.html'),
         name='password_reset'),
         path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='dashboard/password_reset_done.html'),
         name='password_reset_done'), 
         path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='dashboard/password_reset_confirm.html'),
         name='password_reset_confirm'), 
         path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='dashboard/password_reset_complete.html'), name='password_reset_complete'),
         # Had heart attack before realising i needed this here. 
         path('assignment/<int:assignment_id>/contact/', views.contact_assignment_creator, name='contact_assignment_creator'),
]