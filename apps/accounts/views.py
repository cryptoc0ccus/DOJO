from django.contrib.auth.views import PasswordResetConfirmView
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate

from .forms import RegistrationForm, AccountAuthenticationForm, UploadDocumentForm
from django.conf import settings
from .decorators import *
from django.contrib.auth.models import Group
from django_require_login.decorators import public


###########

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
#from core.forms import SignUpForm, ProfileForm
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
################
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
#####################

# Create your views here.

from apps.datatables.models import Document

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

    try:
        if request.user.student.qr_code:
            has_qr_code = True
    except:
        pass

    


# Documents Uploader:
    form = ''
    std_id = ''
    try:
        if request.user.student:
        #std_id = request.user.student.id
            std_id = request.user.student
            form = UploadDocumentForm(initial={"student" :std_id})
            if request.method == 'POST':
                form = UploadDocumentForm(request.POST,request.FILES, initial={"student" :std_id})
                if form.is_valid():
                    std_id.upload_counter += 1
                    std_id.save()
                    form.save()
                    messages.success(request, 'File uploaded successfully')
                    return redirect('accounts:home')
                else:
                    form = UploadDocumentForm(initial={"student" :std_id})
    except:
        pass





 



    return render(request, 'home.html', {'user' :user, 'has_profile' :has_profile,
                'has_subscription' :has_subscription, 
                'has_free_subscription' :has_free_subscription, 
                'has_qr_code' :has_qr_code, 
                'form' :form, 'std_id' :std_id})

#@unauthenticated_user
@public
def register_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():            
            user = form.save()
            user.is_active = False # Testing the email confirmation
            user.save()
            #login(request, user)    #deactivated for testing

            # return redirect('../')

            current_site = get_current_site(request)

            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            from_email = 'noreply@bjj.berlin'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, from_email, to=[to_email]
            )
            email.send() 

            return HttpResponse('Please confirm your email address to complete the registration')      
            # group = Group.objects.get(name='student')  
            # user.groups.add(group) 
           
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

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode


from django.contrib.auth import get_user_model
from django.contrib import messages




@public
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    #    user = get_user_model()
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Thank you for your email confirmation. Now you can use your account.')
        return redirect('accounts:home')
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


from django.utils.decorators import method_decorator

@public
class MyPasswordResetConfirmView(PasswordResetConfirmView):
    @method_decorator(public)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

def access_token(request, token):
   pass


def delete_account(request):
    User = get_user_model()
    user = User.objects.get(pk=request.user.pk)
    if request.POST:
        logout(request)
        try:
            if user.student:
                user.student.delete()
        except: 
            pass
        
        user.delete()
        messages.success(request, 'Your account has been successfully deleted.')

        return redirect('accounts:home')
    
    return render(request, "delete.html", {'user' :user})