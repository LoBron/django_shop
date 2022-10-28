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


class Address(models.Model):
    user = models.ForeignKey(
        User, verbose_name=_('User'),
        blank=True, null=True,
        on_delete=models.CASCADE
    )
    city = models.CharField(_('City'), max_length=100)
    street = models.CharField(_('Street'), max_length=100)
    house = models.CharField(_('House'), max_length=10)
    building = models.CharField(_('Building'), max_length=10, blank=True, null=True)
    porch = models.CharField(_('Porch'), max_length=10)
    floor = models.CharField(_('Floor'), max_length=20, blank=True, null=True)
    door = models.CharField(_('Door'), max_length=20)

    # country = models.CharField(_('Country'), max_length=100, blank=True)

    def __str__(self):
        return f'г. {self.city}, ул. {self.street}, д.{self.house} к. {self.building},' \
               f' под. {self.porch}, эт. {self.floor}, кв. {self.door}'
