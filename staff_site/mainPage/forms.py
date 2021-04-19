from django_otp.forms import OTPAuthenticationForm
from django import forms
from django_otp.models import Device, VerifyNotAllowed


class SimpleOTPAuthenticationForm(OTPAuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SimpleOTPAuthenticationForm, self).__init__(args, kwargs)

    otp_device = forms.CharField(required=False, widget=forms.HiddenInput)
    otp_challenge = forms.CharField(required=False, widget=forms.HiddenInput)