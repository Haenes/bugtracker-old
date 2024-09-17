from typing import Any

from django.conf import settings
from django.utils.log import AdminEmailHandler

from bugtracker.tasks import send_email


class CustomAdminEmail(AdminEmailHandler):
    def send_mail(
            self,
            subject: str,
            message: str,
            *args: Any,
            **kwargs: Any
            ) -> None:

        send_email.delay_on_commit(
            subject=subject,
            body=message[:34] + message[438:490],
            to_email=[a[1] for a in settings.ADMINS]
            )
