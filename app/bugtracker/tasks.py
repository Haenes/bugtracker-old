from celery import shared_task

from django.core.mail import EmailMessage


@shared_task
def send_email(subject: str, message: str, to_email: list[str]):

    """ Task to send email for verification after registration. """

    email = EmailMessage(subject=subject, body=message, to=to_email)
    email.send()
