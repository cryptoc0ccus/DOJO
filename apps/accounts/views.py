from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, AccountAuthenticationForm
from django.conf import settings

# Create your views here.

def home(request):
    return render(request, 'home.html')

def register_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('../home')
    else:
        form = RegistrationForm()
    context['form'] = form
    context['recaptcha_site_key'] = settings.GOOGLE_RECAPTCHA_SITE_KEY
    return render(request, "register.html", context)

    return render(request, 'register.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('../home')


    context = {}
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('../home')
    else:
        form = AccountAuthenticationForm()
    context['form'] = form
    context['recaptcha_site_key'] = settings.GOOGLE_RECAPTCHA_SITE_KEY
    return render(request, "login.html", context)

def logout_view(request):
    logout(request)
    return redirect("core:index")