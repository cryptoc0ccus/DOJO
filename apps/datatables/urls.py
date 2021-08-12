from .views import *
from django.urls import path, reverse_lazy
from apps.datatables import views as v


from django.conf import settings
from django.conf.urls.static import static


app_name = 'datatables'

urlpatterns = [
    path('', StudentList.as_view(), name='Students'),
    path('profile/<str:pk>/', StudentDetail.as_view(), name='Student'),
    path('create/', StudentCreate.as_view(), name='Student-create'),
    path('update/<str:pk>/', StudentUpdate.as_view(), name='Student-update'),
    path('delete/<str:pk>/', StudentDelete.as_view(), name='Student-delete'),

## Graduation
    path('graduation/update/<str:pk>/', GraduationUpdate.as_view(), name='Graduation-update'), 

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

