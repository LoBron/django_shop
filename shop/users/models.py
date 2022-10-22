from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            # 'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), unique=True)
    email_verify = models.BooleanField(_('email confirmed'), default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
