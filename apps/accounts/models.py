from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
import uuid



# Create your models here.
class AccountManager(BaseUserManager):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)

    def create_user(self, email, password):
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)


class Account(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)

    email = models.EmailField(verbose_name="E-Mail", max_length=60, unique=True)


    # Standard Stuff
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    #
    USERNAME_FIELD = 'email'

    objects = AccountManager()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(selfself, app_label):
        return True

