import random

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    hash = models.CharField('Hash', max_length=128, default=random.getrandbits(128), unique=True)
    birthday = models.DateField(_('Birthday'), null=True)


