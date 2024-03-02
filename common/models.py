from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
	short_description = models.TextField("소개글", blank=True)
	verification_code = models.CharField(max_length=6, blank=True, null=True)
	is_verified = models.BooleanField(default=False)
