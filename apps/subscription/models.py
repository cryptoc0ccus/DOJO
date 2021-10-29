from django.db import models
from django.db.models.base import Model
from DOJO import settings
import uuid

# Create your models here.

class Customer(models.Model):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    stripeid = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)
    cancel_at_period_end = models.BooleanField(default=False)
    membership = models.BooleanField(default=False)
    last4 = models.CharField(max_length=4, null=True)
    mandate_ref = models.CharField(max_length=20, null=True)
    plan = models.CharField(max_length=20, null=True)

    def __str__(self):
        return str(self.user)

class Member(models.Model):
    is_member = models.BooleanField(default=True)
