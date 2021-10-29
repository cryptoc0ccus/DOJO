from django.urls import path, reverse_lazy
from apps.accounts import views as v
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from .views import *
from django.conf.urls import url

app_name = 'accounts'

urlpatterns = [
     path('', v.home, name='home'),
     path('login/', v.login_view, name="user_login"),
     path('register/', v.register_view, name="user_register"),
     path('logout/', v.logout_view, name="user_logout"),

    
    #password reset:

    path('password_reset/', auth_views.PasswordResetView.as_view(
        email_template_name = 'registration/password_reset_email.html',
        success_url=reverse_lazy('accounts:password_reset_done')
    ), name='password_reset'),

    path('password_reset_sent/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', v.MyPasswordResetConfirmView.as_view(template_name="registration/password_reset.html"), 
    name='password_reset_confirm'),


    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),            
            name='password_reset_complete'),

    path('activate/<uidb64>/<token>/',  v.activate, name='activate'),

    path('delete_account/', v.delete_account, name='delete_account')




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





