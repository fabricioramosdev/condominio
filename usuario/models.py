import os
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


def path_and_rename(instance, filename):
    upload_to = 'profiles/'
    ext = filename.split('.')[-1]

    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    return os.path.join(upload_to, filename)


class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)

    profile_image = models.ImageField(
        null=True, blank=True, upload_to=path_and_rename, default="profiles/user-default.png")

    criado = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(_('Status'), default=True, null=False, blank=False)

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ['criado']

    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url