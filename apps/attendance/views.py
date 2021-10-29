from django.shortcuts import render
from .models import *

from django.shortcuts import render, redirect

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from apps.attendance.forms import ContactForm
from django_require_login.decorators import public


def displayqrcode(request):
    qr_code = request.user.student.qr_code
    context = {'qr_code' :qr_code}

    return render(request, 'member_qrcode.html', context )


@public
def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "email_visitor.html", {'form': form})

@public
def successView(request):
    return HttpResponse('Success! Thank you for your message.')