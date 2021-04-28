from django.conf import settings
from django.contrib.auth import get_user_model

from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = settings.ADMIN_EMAIL
        if not User.objects.filter(email=email).exists():
            password = settings.ADMIN_PASSWORD
            User.objects.create_superuser(
                email,
                password
            )
