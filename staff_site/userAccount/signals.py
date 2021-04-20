import datetime
import hashlib
import io
import random
import secrets

import qrcode
from django.core.mail import send_mail, EmailMessage
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from hashlib import sha1
from random import randint
from .models import InternalUser
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.core import signing
from django.core.signing import Signer
MIN_CODE = 100000
"""int: the smallest number that can be code of key
"""

MIN_LINKING_CODE = 10000
"""int: the smallest number that can be linking code of lock
"""

MAX_LINKING_CODE = 99999
"""int: the largest number that can be linking code of lock
"""

MAX_CODE = 999999999
"""int: the largest number that can be code of key
"""


@receiver(post_save, sender=InternalUser, weak=False)
def create_linking_code(sender: InternalUser.__class__, instance, created, **kwargs):
    """Generates and saves a random number in the linking_code field just before saving lock in database.
    """
    if created:
        device = instance.totpdevice_set.create(confirmed=True)
        url = device.config_url
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = io.BytesIO()
        qr.make_image().save(img, 'PNG')
        img.seek(0)
        filename = 'qrcode-code1.png'
        message = "Вопспользуйтесь Google Authenticator для получения доступа к " \
                  "аккаунту."
        subject = "2FA"
        send_from = "INTERNAL SECURITY <internal_security@lockandrent.ru>"
        mail = EmailMessage(subject=subject, body=message, from_email=send_from, to=[instance.email])
        mail.attach(filename, img.getvalue(), 'image/png')
        mail.send()
