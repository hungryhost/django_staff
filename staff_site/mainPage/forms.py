from django_otp.forms import OTPAuthenticationForm
from django import forms
from django_otp.models import Device, VerifyNotAllowed


class SimpleOTPAuthenticationForm(OTPAuthenticationForm):
    otp_device = forms.CharField(required=False, widget=forms.HiddenInput)
    otp_challenge = forms.CharField(required=False, widget=forms.HiddenInput)