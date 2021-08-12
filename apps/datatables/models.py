import hashlib
from datetime import date
from django.db.models.signals import post_save
from PIL import Image
from dateutil.relativedelta import relativedelta
from django.core.validators import MaxValueValidator
from django.db import models
from django.dispatch import receiver
from apps.accounts.models import *
from django.conf import settings
from DOJO import settings

def upload_location(instance, filename, **kwargs):
    file_path = 'profile_images/{filename}'.format(
        filename=hashlib.md5(str(instance.address + instance.first_name + instance.last_name).encode()).hexdigest() + settings.os.path.splitext(filename)[1])
    return file_path

# Create your models here.
class Student(models.Model):
    def __str__(self):
        return self.first_name + " " + self.last_name

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    first_name = models.CharField("First name", max_length=30, default="", null=True)
    last_name = models.CharField("Last name", max_length=30, default="", null=True)    
    phone = models.CharField("Phone", max_length=30, default="", null=True)
    birth_date = models.DateField(blank=False, null=True, validators=[MaxValueValidator(limit_value=date.today)])
    address = models.CharField("Address", blank=False, max_length=200, default="", null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    gender_selector = (
        ('0', ''),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(
        "Gender",
        max_length=6,
        choices=gender_selector,
        null=True,
        blank=True)
    profile_img = models.ImageField(upload_to=upload_location, null=True, blank=True)

    class Meta:
        ordering = ['first_name']
        verbose_name = 'student'
        verbose_name_plural = 'students'


    @property
    def age(self):
        if (self.birth_date != None):
            age = date.today().year - self.birth_date.year
            return age

    ### Media ##
  #  hashlib



@receiver(post_save, sender=Student)
def post_save_compress_img(sender, instance, *args, **kwargs):
    if instance.profile_img:
        picture = Image.open(instance.profile_img.path)
        picture.save(instance.profile_img.path, optimize=True, quality=30)



## Graduation
class Graduation(models.Model):
    BELT_SELECTOR = (
        ('WHITE', 'WHITE'),
        ('BLUE', 'BLUE'),
        ('PURPLE', 'PURPLE'),
        ('BROWN', 'BROWN'),
        ('BLACK', 'BLACK'),
    )
    STRIPE_SELECTOR = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    )
    belt = models.CharField(max_length=6, choices=BELT_SELECTOR, default="")
    stripe = models.CharField(max_length=1, choices=STRIPE_SELECTOR, default="")
    belt_since = models.DateField("Last Graduation", blank="True", null=True, validators=[MaxValueValidator(limit_value=date.today)])

    # membership Inheritance
    graduation = models.OneToOneField(Student, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.graduation)


