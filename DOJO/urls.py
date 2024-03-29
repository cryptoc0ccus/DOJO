from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('apps.accounts.urls')),
    #path('', include('apps.core.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    path('students/', include('apps.datatables.urls')),
    path('subscription/', include('apps.subscription.urls')),
    path('attendance/', include('apps.attendance.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
