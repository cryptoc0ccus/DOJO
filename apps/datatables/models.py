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
    profile_img = models.ImageField(upload_to=upload_location, null=True, blank=True,  default = '../media/profile_images/no-img.png')

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


## Sending a signal to create graduation after Student is created.
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=Student)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        graduation = Graduation(graduation=instance)
        print('graduation created')
        graduation.save()


### Membership
from dateutil.relativedelta import relativedelta
from django.core.validators import MaxValueValidator

class Membership(models.Model):
    member_since = models.DateField("Member since", blank=False, null=True,
                                    validators=[MaxValueValidator(limit_value=date.today)])
    autorenew_membership = models.BooleanField(default=True)
    ACTIVE_MEMBER = (
        ('ACTIVE', 'ACTIVE'),
        ('INACTIVE', 'INACTIVE'),
        ('PAUSED', 'PAUSED'),

    )
    membership_status = models.CharField("Status", max_length=8, choices=ACTIVE_MEMBER, default="")
    activation_date = models.DateField('date activated', null=True)  # timestamp when membership got activated

    MEMBERSHIP_SELECTOR = (
        ('GOLD', 'GOLD'),
        ('SILVER', 'SILVER'),
        ('BRONZE', 'BRONZE'),
    )
    membership_type = models.CharField("Type", max_length=6, choices=MEMBERSHIP_SELECTOR, default="")
    PERIOD_SELECTOR = (
        ('12 Months', '12 Months'),
        ('6 Months', '6 Months'),
        ('3 Months', '3 Months'),
    )
    membership_period = models.CharField("Period", max_length=10, choices=PERIOD_SELECTOR, default="")

    # membership Inheritance
    membership = models.OneToOneField(Student, null=True, on_delete=models.CASCADE)  

    # Set activation date as status changes. -> Could it be done using another signal ???

    def save_timestamp(self, *args, **kwargs):
        if self.membership_status == 'ACTIVE' and self.activation_date is None:
            self.activation_date = date.today()
        elif self.membership_status == 'INACTIVE' and self.activation_date is not None:
            self.activation_date = None
        super(Membership, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' % self.membership
        

    #Same here: Student profile is created, membership is created
    @receiver(post_save, sender=Student)
    def create_profile_for_new_user(sender, created, instance, **kwargs):
        if created:
            membership = Membership(membership=instance)
        print('membership created')
        membership.save()



    @property
    def membership_expiration(self):
        expiration_date = 'EXPIRED'
        if self.membership_status == 'ACTIVE':
            if self.membership_period == '12 Months':
                duration_months = 12
                expiration_date = self.activation_date + relativedelta(months=+duration_months)
            elif self.membership_period == '6 Months':
                duration_months = 6
                expiration_date = self.activation_date + relativedelta(months=+duration_months)
            else:
                duration_months = 3
                expiration_date = self.activation_date + relativedelta(months=+duration_months)

            if self.autorenew_membership:
                new_expiration_date = expiration_date + relativedelta(months=+duration_months)
                if expiration_date == date.today():
                    expiration_date = new_expiration_date

        return expiration_date


## POSTS

class Posts(models.Model):
    SUBJECT_SELECTOR = (
        ('Technique', 'Technique'),
        ('Warning', 'Warning'),
        ('Graduation', 'Graduation'),
    )
    posts = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    posts_category = models.CharField(max_length=15, choices=SUBJECT_SELECTOR,
                                      default='')
    posts_created_on = models.DateField(blank="True", null=True)
    posts_content = models.TextField()

    class Meta:
        ordering = ['posts_created_on']


    def __str__(self):
        return '%s' % self.posts_category
