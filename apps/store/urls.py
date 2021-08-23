from django.urls import path, reverse_lazy
from apps.store import views as v
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'store'

urlpatterns = [
     path('pricing_page/', v.pricing_page, name='pricing_page'),
     path(
        "checkout/",
        v.CreateCheckoutSessionView.as_view(),
        name="checkout",
    ),
     path(
        "purchase-subscription",
        v.PurchaseSubscriptionView.as_view(),
        name="purchase_subscription",
     ),
     path(
        "purchase-subscription-success/<id>",
        v.PurchaseSubscriptionSuccessView.as_view(),
        name="purchase_subscription_success",
     ),
     path("payment-intent", v.create_payment_intent, name="payment_intent"),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





