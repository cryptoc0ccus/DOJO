from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
import hashlib
from apps.datatables.models import Membership
import uuid

from django.dispatch import receiver


# Create your models here.
class Member(models.Model):
    member = models.OneToOneField(Membership, null=True, on_delete=models.CASCADE)
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
   # name = models.CharField(max_length=200)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def __str__(self):
        return str(self.id)
        
    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.id)
        canvas = Image.new('RGB', (340, 340), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.id}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(args, **kwargs)

# @receiver(post_save, sender=Membership)
# def create_qrcode_for_new_user(sender, created, instance, **kwargs):

    # if created:
    #     graduation = Graduation(graduation=instance)
    #     print('graduation created')
    #     graduation.save()