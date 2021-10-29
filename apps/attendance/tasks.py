from django.utils import timezone
from apps.datatables.models import Student
from django.contrib.auth import get_user_model
import stripe
import datetime
from django.core.mail import EmailMessage, send_mail

User = get_user_model()
users = User.objects.all()


#     """
#    Searches for and deletes all qr_codes that are expired
#     """



def check_expired_memberships():  
    print('checking for expired memberships') 
    #User = get_user_model()
    #users = User.objects.all()
    global users
    for user in users:
        try:
            if user.student:
                if user.student.membership.is_active:
                    if user.student.membership.expiry_date < datetime.date.today():
                        if not user.student.membership.autorenew_membership:                      

                            user.student.membership.is_active = False
                            user.student.membership.save_timestamp()
                            user.student.membership.save()
        except:
            pass
    
    # Check Age here

def check_age():
    print('checking for ages')
    global users
    today = timezone.now().date()
   
    for user in users:
        try:
            if user.student: 
                day = user.student.birth_date.day
                month = user.student.birth_date.month
                if day == today.day and month == today.month:
                    subject = 'Happy birthday %s !' % user.student.first_name
                    body = 'Hi %s,\n We Wish you happy birthday \n May this next year be full of Jiu-Jitsu! \n Your Dojo' % user.student.first_name
                    send_mail(subject, body, 'admin@bjj.berlin', [user.email])
                    if user.student.age == 14:
                        user.student.is_kid = False
                        user.student.is_teen = True
                        user.student.save()
                    if user.student.age >= 14 and user.student.age < 18:
                        user.student.is_kid = False
                        user.student.is_teen = True
                        user.student.save()
                    if user.student.age >= 18:
                        user.student.is_kid = False
                        user.student.is_teen = False
                        user.student.save()

        except:
            pass


def send_payment_notification():
    pass

