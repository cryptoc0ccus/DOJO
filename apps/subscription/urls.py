from .views import *
from django.urls import path, reverse_lazy
from apps.subscription import views as v


from django.conf import settings
from django.conf.urls.static import static


app_name = 'subscription'

urlpatterns = [
    path('terms', v.terms, name='terms'),
    path('join', v.join, name='join'),
  #  path('checkout', v.checkout, name='checkout'),
    path('checkout_sepa', v.checkout_sepa, name='checkout_sepa'),
    path('', v.subscription, name='subscription'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

