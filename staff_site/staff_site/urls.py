"""staff_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django_otp.admin import OTPAdminSite
from django_otp.plugins.otp_totp.models import TOTPDevice
from two_factor.urls import urlpatterns as tf_urls

from mainPage.forms import SimpleOTPAuthenticationForm

User = get_user_model()

class OTPAdmin(OTPAdminSite):
    pass


admin_site = OTPAdmin(name='OTPAdmin')
admin_site.register(User)
admin_site.register(TOTPDevice)

urlpatterns = [
	path('admin2/', admin_site.urls),
	path('admin/', admin.site.urls),
	path('staff/', include(tf_urls)),
	path('', include('mainPage.urls')),
	path('sales/', include('sales.urls')),
	path('manufacturing/', include('manufacturing.urls')),
	path('login/', auth_views.LoginView.as_view(
		template_name='mainPage/login.html',
		authentication_form=SimpleOTPAuthenticationForm),
		name='login'),
	path('password_reset/', auth_views.PasswordResetView.as_view(
		template_name='registration/password_reset_form.html'
	), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
		template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>)/',
        auth_views.PasswordResetConfirmView.as_view(
	        template_name='registration/password_reset_confirm.html'
        ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
		template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
	path('logout/', auth_views.LogoutView.as_view(
		template_name='mainPage/logout.html'), name='logout'),
	url(r'^newsletter/', include('newsletter.urls')),
	re_path(r'^watchman/', include('watchman.urls')),
	]
