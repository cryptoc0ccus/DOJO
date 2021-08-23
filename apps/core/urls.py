from django.urls import path, reverse_lazy
from apps.core import views as v
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'core'

urlpatterns = [
     path('', v.index, name='index'),
     path('dashboard/', v.dashboard, name='dashboard'),
     path('dashboard-admin/', v.dashboard_admin, name='dashboard-admin'),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


