from django.contrib.auth.models import User, AbstractUser
from django.db import models
import os


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)


class CustomUser(AbstractUser):
    birth_date = models.DateTimeField(
        blank=True, null=True)
    information = models.TextField()
    profile_image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
