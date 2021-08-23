from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('accounts/', include('apps.accounts.urls')),
    path('', include('apps.core.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    path('students/', include('apps.datatables.urls')),
    path('store/', include('apps.store.urls')),
    path("stripe/", include("djstripe.urls", namespace="djstripe")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
