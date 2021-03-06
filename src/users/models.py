from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def tokens(self):
        token = RefreshToken.for_user(self)
        return {
            'refresh': str(token),
            'access': str(token.access_token)
        }


class VerificationCode(models.Model):
    email = models.EmailField('Email attached to the verification code')
    code = models.CharField(max_length=6, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email} - {self.code[0]}****{self.code[-1]}'


class GenderChoices(models.TextChoices):
    MALE = ('MALE', '??????????????')
    FEMALE = ('FEMALE', '??????????????')
    OTHER = ('OTHER', '????????????')


class UserProfile(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=16,
        blank=True
    )
    username = models.CharField(
        max_length=100,
        blank=True
    )
    gender = models.CharField(
        max_length=100,
        choices=GenderChoices.choices,
        blank=True
    )
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='profile'
    )
    achievements = models.ManyToManyField(
        to='notifications.Achievement',
        blank=True
    )
    photo = models.ForeignKey(
        to='files.ProfilePhoto',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )


@receiver(post_save, sender=User, dispatch_uid="create_profile")
def update_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
