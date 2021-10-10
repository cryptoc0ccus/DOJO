from .views import *
from django.urls import path, re_path
from apps.datatables import views as v


from django.conf import settings
from django.conf.urls.static import static


app_name = 'datatables'

urlpatterns = [
    path('', StudentList.as_view(), name='Students'),
    path('profile/<str:pk>/', StudentDetail.as_view(), name='Student'),
    #path(r'^profile/$', StudentDetail.as_view(), name='Student'),
    path('create/', StudentCreate.as_view(), name='Student-create'),
    path('update/<str:pk>/', StudentUpdate.as_view(), name='Student-update'),
    path('delete/<str:pk>/', StudentDelete.as_view(), name='Student-delete'),

## Graduation
    path('graduation/update/<str:pk>/', GraduationUpdate.as_view(), name='Graduation-update'), 
## Membership
    path('membership/update/<str:pk>/', MembershipUpdate.as_view(), name='Membership-update'), 
     path('membership/display/<str:pk>/', MembershipDisplay.as_view(), name='Membership-display'), 

## Posts
    path('posts/create/<str:pk>/', PostCreate.as_view(), name='Post-create'),
    path('posts/delete/<str:pk>/', PostDelete.as_view(), name='Post-delete'),  
    path('posts/list/<str:pk>', PostsList.as_view(), name='Post-list'),  
## Documents
    path('documents/upload/<str:pk>/', DocumentsCreate.as_view(), name='document-upload'),
   # path('documents/list/<str:pk>/', DocumentList.as_view(), name='document-list'), 
    path('documents/delete/<str:pk>/', DocumentsDelete.as_view(), name='document-delete'),

## QR CODE
    path('qrcode/', v.manage_qrcode, name='manage_qrcode'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

