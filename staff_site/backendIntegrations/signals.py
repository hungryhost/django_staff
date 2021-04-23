import datetime
import secrets
from io import BytesIO

import uuid
from django.core.files import File

from manufacturing.pdf_generator import PdfGenerator
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from hashlib import sha1
from random import randint
from .models import RegisterLock, RegisterCard, RegisterKey, LockManuals, LockGeneratedUserFiles
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


@receiver(pre_save, sender=RegisterLock, weak=False)
def hash_lock_id(sender: RegisterLock.__class__, **kwargs):
    """Hashes uuid of lock just before saving it in database.
    """
    new_lock = kwargs['instance']
    new_lock.uuid = uuid.uuid4()
    new_lock.hash_id = sha1(str(new_lock.uuid).encode('utf-8')).hexdigest()


@receiver(pre_save, sender=RegisterCard, weak=False)
def hash_card_id(sender: RegisterCard.__class__, **kwargs):
    """Hashes card_id of card just before saving it in database.
    """
    new_card = kwargs['instance']
    new_card.hash_id = sha1(str(new_card.card_id).encode('utf-8')).hexdigest()


def secure_code(key: RegisterKey, code: int):
    data_to_sign = {
        "code": code,
        "expires_at_dt": key.access_stop.strftime('%Y-%m-%dT%H:%M:%S%z'),
        "expires_seconds": str((key.access_stop - key.access_start).total_seconds()),
        "lock_id": key.lock.id,
        "signed_at": datetime.datetime.now().timestamp()
    }
    return signing.dumps(data_to_sign)


@receiver(pre_save, sender=RegisterKey, weak=False)
def hash_code(sender: RegisterKey.__class__, **kwargs):
    """Generates and saves a random number in the code field. Hashes generated code of key just before saving it in
    database.
    """
    new_key = kwargs['instance']
    if not new_key.code:
        code = randint(MIN_CODE, MAX_CODE)
        new_key.code = code
        new_key.code_secure = secure_code(new_key, code)
        new_key.hash_code = sha1(str(code).encode('utf-8')).hexdigest()
    else:
        code = new_key.code
        new_key.created_manually = True
        new_key.code_secure = secure_code(new_key, code)
        new_key.hash_code = sha1(str(code).encode('utf-8')).hexdigest()


@receiver(post_save, sender=RegisterLock, weak=False)
def generate_user_file(sender: RegisterLock.__class__, instance, created, **kwargs):
    """Generates and saves a random number in the linking_code field just before saving lock in database.
    """

    if created:
        id_string = str(instance.id)
        # Define our random string alphabet (notice I've omitted I,O,etc. as they can be confused for other characters)
        upper_alpha = "ABCDEFGHJKLMNPQRSTVWXYZ"
        # Create an 8 char random string from our alphabet
        random_str = "".join(secrets.choice(upper_alpha) for i in range(8))
        # Append the ID to the end of the random string
        instance.linking_code = (random_str + id_string)[-8:]
        instance.save()

        key = RegisterKey(
            lock=instance,
            access_start=datetime.datetime.now(),
            access_stop=datetime.datetime(2099, 12, 31, 23, 59, 59),
            is_master=True
        )
        key.save()

        if str(instance.version) == '1':
            version = 'Ethernet'
        elif str(instance.version) == '2':
            version = 'Wi-Fi'
        else:
            version = 'Custom'

        generated_file = PdfGenerator(
            data={
                "linking_code": instance.linking_code,
                "hash_id": instance.hash_id,
                "version": version,
                "firmware": instance.firmware,
                "uuid": instance.uuid,
                "created_at": instance.created_at,
                "keys": key.code
            },
            pdf_template_path='pdf_generator/owner_file.html').generate()
        filename = "PDF_USER_GUIDE{}.pdf".format(str(instance.id))
        db_gen = LockGeneratedUserFiles(
            filename=filename,
            lock=instance,
            file=File(BytesIO(generated_file), name=filename))
        db_gen.save()


@receiver(post_delete, sender=LockManuals)
def remove_file_from_s3(sender, instance, using, **kwargs):
    try:
        instance.file.delete(save=False)
    except Exception as e:
        pass


@receiver(post_delete, sender=LockGeneratedUserFiles)
def remove_file_from_s3(sender, instance, using, **kwargs):
    try:
        instance.file.delete(save=False)
    except Exception as e:
        pass