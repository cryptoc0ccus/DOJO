from .views import *
from django.urls import path, reverse_lazy
from apps.attendance import views as v


from django.conf import settings
from django.conf.urls.static import static


app_name = 'attendance'

urlpatterns = [
   path('qrcode/', v.displayqrcode, name='display-qrcode'),   
   path('contact/', v.contactView, name='contact'),
   path('success/', v.successView, name='success'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

