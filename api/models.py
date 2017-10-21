# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import six, timezone
from django.utils.translation import ugettext_lazy as _
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.create_user(email, password, **extra_fields)
        user.is_admin = True

        user.save(using=self._db)
        return user


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=150,
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_owner = models.BooleanField(
        _('owner status'),
        default=False,
        help_text=_('Designates whether the user is an owner of a food truck'),
    )
    USERNAME_FIELD = 'email'


    objects = UserManager()

    def clean(self):
        super(User, self).clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """

        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name.strip()


class Truck(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='Food Truck')
    description = models.CharField(max_length=500, default='Default Description')

    def __str__(self):
        return self.title


def hour_later():
    return timezone.now() + timezone.timedelta(hours=1)


class Post(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now, help_text='Start time for opening')
    end_time = models.DateTimeField(
        default= hour_later,
        help_text='End time for opening'
    )

    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=0.0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=0.0)






