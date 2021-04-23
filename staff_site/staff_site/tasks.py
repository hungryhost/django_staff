from celery import shared_task
from celery.decorators import task
from celery.utils.log import get_task_logger
from time import sleep
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.management import call_command
from django.template import Context
from django.template.loader import get_template
from django.conf import settings
logger = get_task_logger(__name__)


@task(name="send_submissions")
def send_submissions():
    """
    This method removes all blacklisted tokens.
    Version: 1.0
    """
    # local import of model, otherwise it won't work
    from newsletter.models import Submission
    Submission.submit_queue()
