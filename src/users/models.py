from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import UserManager
from django.core.mail import send_mail

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model.
    Email is user as a Username Field.
    """
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=30)
    last_name = models.CharField('last name', max_length=30)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Custom User Manager
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_name(self):
        """
        Return full name of the User.
        """
        return "{} {}".format(self.first_name, self.last_name)

    def send_verification_email(self, subject, message, from_email=None, **kwargs):
        """
        Send account verification email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)



