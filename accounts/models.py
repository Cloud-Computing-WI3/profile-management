from uuid import uuid4
import os

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from categories.models import Category
from keywords.models import Keyword

from .managers import AccountManager

def user_picture_path(instance, filename):
    upload_to = "profiles/avatars/"
    ext = filename.split('.')[-1]
    if len(ext) > 3:
        ext = "jpg"
    # get filename
    if instance.pk:
        filename = 'avatar_{}-{}-{}.{}'.format(instance.given_name, instance.family_name, instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class Account(AbstractBaseUser, PermissionsMixin):

    # Account attributes
    email = models.EmailField(_('email address'), unique=True)
    given_name = models.CharField(_("given name"), max_length=25)
    family_name = models.CharField(_("family name"), max_length=25)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    picture = models.ImageField(upload_to=user_picture_path, blank=True, null=True)
    categories = models.ManyToManyField(Category)
    keywords = models.ManyToManyField(Keyword)

    # Set user is identified by email and has to be registered with a valid email
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return "{} {}".format(self.given_name, self.family_name)
