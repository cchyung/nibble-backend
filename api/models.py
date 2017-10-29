# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import six, timezone
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid, re
from django.template.defaultfilters import slugify


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
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)

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
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='Food Truck')
    description = models.CharField(max_length=500, blank=True)
    genre = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=150, blank=True)
    phone = models.CharField(max_length=9, blank=True)

    def validate_phone(value):
        pattern = re.compile("^\d{10}$")
        if not pattern.match(value):
            raise ValidationError(
                _('%(value)s is not a valid phone number'),
                params={'value': value}
            )

    def __str__(self):
        return self.title



class LikedTruck(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unique_together = ('truck', 'user')

    def __str__(self):
        return self.truck.title + " - " + self.user.get_full_name()


class TruckRating(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(3), MinValueValidator(1)])
    unique_together = ('truck', 'user')


class MenuItem(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='')
    slug = models.SlugField(max_length=100)
    description = models.CharField(max_length=1000, blank=True)
    details = models.CharField(max_length=1000, blank=True)  # For toppings, add-ons, etc.
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True)
    unique_together = ('truck', 'name')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(MenuItem, self).save(*args, **kwargs)


# Helper methods for post model
def round_up_time(time=timezone.now()):
    time -= timezone.timedelta(minutes=(time.minute % 5))
    time = time.replace(second=0, microsecond=0)
    return time

def hour_later():
    time = timezone.now() + timezone.timedelta(hours=1)
    return round_up_time(time)


class Post(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=0.0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=0.0)
    start_time = models.DateTimeField(
        default=round_up_time,
        help_text='Start time for opening'
    )
    end_time = models.DateTimeField(
        default= hour_later,
        help_text='End time for opening'
    )

    def save(self, *args, **kwargs):
        self.start_time = round_up_time(self.start_time)
        self.end_time = round_up_time(self.end_time)
        if self.end_time > self.start_time:
            super(Post, self).save(*args, **kwargs)
        else:
            raise ValidationError('`start_time` cannot be after `end_time`')