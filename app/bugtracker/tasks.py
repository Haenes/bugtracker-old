import logging

from typing import Any
from celery import shared_task

from django.core.mail import EmailMessage
from django.template import loader


logger = logging.getLogger(__name__)


@shared_task
def send_email(
        subject: str,
        body: str,
        to_email: list[str],
        context: dict[str, Any] = None,
        html_email_template_name=None
        ):

    """ The task to send an email to the user,

    when registering or resetting the password.
    """

    if html_email_template_name is not None:
        html_email = loader.render_to_string(
            html_email_template_name,
            context
            )
        email_message = EmailMessage(subject, body, to=to_email)
        email_message.attach_alternative(html_email, "text/html")
    else:
        email_message = EmailMessage(subject, body, to=to_email)

    try:
        email_message.send()
    except Exception:
        logger.exception(msg="Failed to send email to the: {to_email[0]}!")
