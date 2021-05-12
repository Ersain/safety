from django.db.utils import IntegrityError
from rest_framework.exceptions import ValidationError

from .models import User


class UserServices:
    @staticmethod
    def reset_password(email, password):
        user = User.objects.filter(email=email)
        if not user.exists():
            return
        user = user.first()
        user.set_password(password)
        user.save()

    @staticmethod
    def update_email_field(user: User, email: str):
        if not email:
            return user
        try:
            user.email = email
            user.save()
        except IntegrityError:
            raise ValidationError('User with that email address already exists!')
        return user
