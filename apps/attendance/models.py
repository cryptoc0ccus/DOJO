from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
import hashlib
from apps.datatables.models import Membership, Student
import uuid

from django.dispatch import receiver


# Create your models here.
class Attendancelist(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)