from random import randint

from django.core.mail import EmailMessage
from rest_framework.exceptions import ValidationError

from .models import VerificationCode

INFO_RECOVERY_CODE_SENT = {
    'info': 'A recovery code has been sent to your email'
}
INFO_PASSWORD_RESET = {
    'info': 'A new password was set'
}
ERROR_INVALID_CREDENTIALS = {
    'error': 'Invalid credentials'
}


class Util:
    @staticmethod
    def generate_verification_code():
        return str(randint(100000, 999999))

    @staticmethod
    def send_mail(subject, body, to: list):
        email = EmailMessage(subject, body, to=to)
        email.send()

    @staticmethod
    def validate_verification_code(email, verification_code):
        data = VerificationCode.objects.filter(
            email__iexact=email,
            code=verification_code
        ).last()

        if not data:
            raise ValidationError(detail=ERROR_INVALID_CREDENTIALS)
        data.delete()
