from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate

from .forms import RegistrationForm, AccountAuthenticationForm
from django.conf import settings
from .decorators import *
from django.contrib.auth.models import Group
from django_require_login.decorators import public


###########

# Create your views here.

def home(request):
    has_profile = False
    has_qr_code = False
    has_subscription = False
    has_free_subscription = False
    user = request.user


    try:
        if request.user.student:
            has_profile = True
            if request.user.student.membership.is_active:
                has_free_subscription = True
                try:
                    if request.user.student.qr_code:
                        has_qr_code = True
                except:
                    pass
    except:
        pass

    try:
        if request.user.customer:
            has_subscription = True
            try:
                if request.user.student.qr_code:
                    has_qr_code = True
            except:
                pass
                        
    except:
        pass



    return render(request, 'home.html', {'user' :user, 'has_profile' :has_profile,
                'has_subscription' :has_subscription, 'has_free_subscription' :has_free_subscription, 'has_qr_code' :has_qr_code })

#@unauthenticated_user
@public
def register_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)    
            # group = Group.objects.get(name='student')  
            # user.groups.add(group) 
            return redirect('../')
    else:
        form = RegistrationForm()
    context['form'] = form
    context['recaptcha_site_key'] = settings.GOOGLE_RECAPTCHA_SITE_KEY
    return render(request, "register.html", context)
    
#@unauthenticated_user
def login_view(request):
    if request.user.is_authenticated:
        return redirect('../')


    context = {}
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('accounts:home')
    else:
        form = AccountAuthenticationForm()
    context['form'] = form
    context['recaptcha_site_key'] = settings.GOOGLE_RECAPTCHA_SITE_KEY
    return render(request, "login.html", context)

def logout_view(request):
    logout(request)
    return redirect("accounts:user_login")


