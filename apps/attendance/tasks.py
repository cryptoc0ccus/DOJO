from django.utils import timezone
from apps.datatables.models import Student
from django.contrib.auth import get_user_model
import stripe
import datetime

User = get_user_model()
users = User.objects.all()


def delete_expired_qrcodes():
    student = Student.objects.all()

#     """
#     Deletes all qr_codes that are more than a minute old
#     """
#     one_minute_ago = timezone.now() - timezone.timedelta(minutes=1)
#     expired_qrcodes = Student.objects.filter(
#         created_at__lte=one_minute_ago
#     )
#     Student.delete_qrcode()

def print_number_1():   
    User = get_user_model()
    users = User.objects.all()
    for user in users:
        try:
            if user.student:
                if user.student.membership.is_active:
                    if user.student.membership.expiry_date == datetime.date.today():
                        print('membership expires today')

        except:
            pass
    
    

