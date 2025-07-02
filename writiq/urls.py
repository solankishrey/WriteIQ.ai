"""
URL configuration for writiq project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from backoffice_engine import views
from backoffice_engine.views import save_generated_content, generate_content, generator, my_generated_content
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.index, name='index'),
    path('app/', views.app, name='app'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/',views.login_view,name='login'),
    path('pricing/', views.pricing, name='pricing'),
    path('generator/', views.generator, name='generator'),
    path('logout/', views.logout, name='logout'),
    path('feedback/', views.submit_feedback, name='feedback'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('help/', views.help, name='help'),
    path('logged_in/', views.logged_in, name='logged_in'),
    path('features/', views.features, name='features'),
    path('profile/', views.profile, name='profile'),
    path('updated_profile/<int:user_id>/', views.update_profile, name='updated_profile'),
    path('delete_account/<int:eid>/', views.delete_account, name='delete_account'),
    path('payment_success/', views.payment_success, name='payment_success'), 
    path('my_generated_content/', views.my_generated_content, name='my_generated_content'),
    path('generate_content/', views.generate_content, name='generate_content'),
    path('generator/', generator, name='generator'),
    path('generate_content/', generate_content, name='generate_content'),
    path('save_generated_content/', save_generated_content, name='save_generated_content'),
    path('my_generated_content/', my_generated_content, name='my_generated_content'),
    path('check/', views.check, name='check'),





 

    ]   