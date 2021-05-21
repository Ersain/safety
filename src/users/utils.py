from random import randint

from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.fields import ChoiceField

from .models import VerificationCode

INFO_RECOVERY_CODE_SENT = {
    'message': 'A recovery code has been sent to your email'
}
INFO_PASSWORD_RESET = {
    'message': 'A new password was set'
}
ERROR_INVALID_CREDENTIALS = {
    'detail': 'Invalid credentials'
}


class AuthenticationException(AuthenticationFailed):
    status_code = status.HTTP_400_BAD_REQUEST


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


class IgnoreCaseChoiceField(ChoiceField):
    def to_internal_value(self, data):
        return super().to_internal_value(str(data).upper())
