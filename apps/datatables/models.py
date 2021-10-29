import hashlib
import os
from datetime import date
from django.db.models.signals import post_save
from PIL import Image
from django.core.validators import MaxValueValidator
from django.db import models
from django.dispatch import receiver
from apps.accounts.models import *
from django.conf import settings
from DOJO import settings
from django.urls import reverse
import uuid

## Sending a signal to create graduation after Student is created.
from django.dispatch import receiver
from django.db.models.signals import post_save


#qrcode
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.core.mail import EmailMessage


def upload_location(instance, filename, **kwargs):
    file_path = 'profile_images/{username}/{filename}'.format(username=instance.user,
        filename=hashlib.md5(str(instance.address + instance.first_name + instance.last_name).encode()).hexdigest() + settings.os.path.splitext(filename)[1])
    return file_path



# Create your models here.
class Student(models.Model):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)

    def __str__(self):
        return self.first_name + " " + self.last_name

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    status_selector = (
        ('Guardian', 'Guardian'),
        ('Visitor', 'Visitor'),
        ('Student', 'Student'),
        ('Staff', 'Staff'),
    ) 

    status = models.CharField(
        "Your status",
        max_length=8,
        choices=status_selector,
        null=True,
        blank=True)

    first_name = models.CharField("First name", max_length=30, default="", null=True)
    last_name = models.CharField("Last name", max_length=30, default="", null=True)    
    phone = models.CharField("Phone", max_length=30, default="", null=True)
    birth_date = models.DateField(blank=False, null=True, validators=[MaxValueValidator(limit_value=date.today)])
    address = models.CharField("Address", blank=False, max_length=200, default="", null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_kid = models.BooleanField(default=False)
    is_teen = models.BooleanField(default=False)
    is_founder = models.BooleanField(default=False)
    upload_counter = models.IntegerField(blank=True, null=True, default=0)
    guardians_name = models.CharField("Guardians name (For all members under 18 years old)", max_length=30, default="", blank=True, null=True)
    
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

    # QRCODE
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def get_absolute_url(self):
        return reverse('datatables:Student', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['first_name']
        verbose_name = 'student'
        verbose_name_plural = 'students'


    @property
    def age(self):
        if (self.birth_date != None):
            age = date.today().year - self.birth_date.year
            if age <= 14:
                self.is_kid = True
                self.save()
            if age > 14 and age < 18:
                self.is_kid = False
                self.is_teen = True
                self.save()
            if age >= 18:
                self.is_kid = False
                self.is_teen = False
                self.save()
            return age


    def save_qrcode(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.id)
        canvas = Image.new('RGB', (340, 340), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.user}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(args, **kwargs)

        print('email sent')
        email_subject = 'Thanks for activating your membership - Here is  your Access code'
        email_message = """ Hello %s ! 
                        Thanks for subscribing !
                        Please keep this QR Code all the time with you, this is the only way to verify your attendance at the Dojo! 
                        See you on the mat !
                        """%self.first_name
        email_from = 'noreply@bjj.berlin'
        email_to = [self.user.email]
        email_file = self.qr_code.path

        qr_mail = EmailMessage(
                                email_subject, 
                                email_message, 
                                email_from, 
                                email_to, 
                                )
        qr_mail.attach_file(email_file)
        qr_mail.send()

    #DELETE QR CODE
    
    def delete_qrcode(self): 
        print('membership expired today, QR CODE DELETED')

        email_subject = 'Your membership has expired'
        email_message = """ Hello %s ! 
                                                Your membership has expired.
                                                Your access code will be deleted. Your Personal data, Graduation and Documents are stored in our server.
                                                You can login and delete them or contact our admin: admin@bjj.berlin
                                                We hope that you will return to the mats. 
                                                See you in the future !
                                                """%self.user.student.first_name
        email_from = 'noreply@bjj.berlin'
        email_to = [self.user.email]                            

        qr_mail = EmailMessage(
            email_subject, 
            email_message, 
            email_from, 
            email_to, 
            )
                            
        qr_mail.send()       
        os.remove(self.qr_code.path)
        self.qr_code.delete()  

@receiver(post_save, sender=Student)
def post_save_compress_img(sender, instance, *args, **kwargs):
    if instance.profile_img:
        picture = Image.open(instance.profile_img.path)
        picture.save(instance.profile_img.path, optimize=True, quality=30)




## Graduation
class Graduation(models.Model):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)



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
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)


    member_since = models.DateField("Member since", blank=False, null=True,
                                    validators=[MaxValueValidator(limit_value=date.today)])
    autorenew_membership = models.BooleanField(default=False)
    ACTIVE_MEMBER = (
        ('ACTIVE', 'ACTIVE'),
        ('INACTIVE', 'INACTIVE'),
        ('PAUSED', 'PAUSED'),

    )
    is_active = models.BooleanField(default=False)   
    activation_date = models.DateField('date activated', blank=True, null=True)  # timestamp when membership got activated
    activation_counter = models.IntegerField(blank=True, null=True, default=0)
    expiry_date = models.DateField('expiry date', blank=True, null=True)  # timestamp when membership got activated
   

    # membership Inheritance
    student = models.OneToOneField(Student, null=True, on_delete=models.CASCADE)  
     

    def __str__(self):
        return '%s' % self.student

    
    # Set activation date as status changes.


    def save_timestamp(self, *args, **kwargs): 
        if self.is_active and self.activation_date is None:
            if self.activation_counter is None:
                self.activation_counter = 0
            self.activation_counter += 1 
            self.activation_date = date.today() 
            #generate qrcode 
            self.student.save_qrcode()         
        elif not self.is_active and self.activation_date is not None:
            self.activation_date = None
            #delete qrcode
            self.student.delete_qrcode()

            print('This student has renewed again :', self.activation_counter)
            super(Membership, self).save(*args, **kwargs)
          
        print(self.activation_counter)


    #Same here: Student profile is created, membership is created
    @receiver(post_save, sender=Student)
    def create_profile_for_new_user(sender, created, instance, **kwargs):
        if created:
            membership = Membership(student=instance)
            print('membership created')            
            membership.save()



## POSTS

class Posts(models.Model):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)

    SUBJECT_SELECTOR = (
        ('Technique', 'Technique'),
        ('Warning', 'Warning'),
        ('Graduation', 'Graduation'),
    )
    
    category = models.CharField(max_length=15, choices=SUBJECT_SELECTOR,
                                      default='')
    created_on = models.DateField(blank="True", null=True, validators=[MaxValueValidator(limit_value=date.today)])
    content = models.TextField()

    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_on']


    def __str__(self):
        return '%s' % self.category


### Documents
def file_location(instance, filename, **kwargs):
    filename = hashlib.md5(str(instance.file.name).encode()).hexdigest() + settings.os.path.splitext(filename)[1] 
    return 'files/{0}/{1}'.format(instance.student.user, filename)

 

class Document(models.Model):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    file = models.FileField('Document', upload_to=file_location)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    
     
    def get_absolute_url(self):
        return reverse('datatables:Document-detail', kwargs={'pk': self.pk})

    def delete(self, *args, **kwargs):
        # first, delete the file
        self.file.delete(save=False)

        # now, delete the object
        super(Document, self).delete(*args, **kwargs)

    def __str__(self):
        return '%s' % self.student

