from django.urls import path, reverse_lazy
from apps.store import views as v
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'store'

urlpatterns = [
     path('', v.store_test, name='store-test'),
     path("checkout", v.checkout, name="checkout"),
 #    path("create-sub", v.create_sub, name="create sub"), #add
 #    path("complete", v.complete, name="complete"), #add

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





