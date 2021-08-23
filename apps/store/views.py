#from apps.store.models import Customer
import json
import logging

import stripe
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import DetailView, FormView
from django.views.generic.base import TemplateView

import djstripe.models
#from djstripe.settings import djstripe_settings

from . import forms






from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from djstripe.models.core import Customer, Product
from apps.accounts.decorators import *
from django.contrib import messages
from DOJO import settings
from django.http import HttpResponse

# Create your views here.
##stripes
import stripe
import djstripe
import djstripe.settings

import json
from django.http import JsonResponse
import djstripe.models
from .forms import PurchaseSubscriptionForm
##
from django.contrib.auth import get_user_model
###
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import DetailView, FormView
from django.views.generic.base import TemplateView
###

User = get_user_model()
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

#USING THE ORM
def pricing_page(request):
    return render(request, 'pricing_page.html', {
        'products': Product.objects.all()
    })




#######################
# 3. Create Session

# price_id = '{{PRICE_ID}}'

# session = stripe.checkout.Session.create(
#   success_url='https://example.com/success.html?session_id={CHECKOUT_SESSION_ID}',
#   cancel_url='https://example.com/canceled.html',
#   payment_method_types=['card'],
#   mode='subscription',
#   line_items=[{
#     'price': price_id,
#     # For metered billing, do not pass quantity
#     'quantity': 1
#   }],
# )

# Redirect to the URL returned on the session
#   return redirect(session.url, code=303)

######################


class CreateCheckoutSessionView(TemplateView):
    
    template_name = "checkout.html"

    def get_context_data(self, **kwargs):
        products = Product.objects.all()
        #Get Parent
        context = super().get_context_data(**kwargs)

        #initialize stripe.js on the frontend
        context['STRIPE_PUBLIC_KEY'] = settings.STRIPE_TEST_PUBLIC_KEY
        context['products'] = products

        success_url = self.request.build_absolute_uri(
            reverse("store:success")
        )

        cancel_url = self.request.build_absolute_uri(reverse("store:pricing_page"))

        try:
            id = djstripe.settings.get_subscriber_model().objects.first().id #djstripe_settings.get_subscriber_model().objects.first().id

        except AttributeError:
            id = (
                djstripe.settings.get_subscriber_model() #settings.djstripe.settings.get_subscriber_model()# get_subscriber_model()
                .objects.create(username="sample@sample.com", email="sample@sample.com")
                .id
            )
        # example of how to insert the SUBSCRIBER_CUSTOMER_KEY: id in the metadata
        # to add customer.subscriber to the newly created/updated customer.
        metadata = {f"{djstripe.settings.SUBSCRIBER_CUSTOMER_KEY}": id}

        session = stripe.checkout.Session.create(
            payment_method_types=["sepa_debit"],
            # payment_method_types=["bacs_debit"],  # for bacs_debit
            payment_intent_data={
                "setup_future_usage": "off_session",
            },
            line_items=[
                {
                    "price_data": {
                        "currency": "eur",
                        # "currency": "gbp",  # for bacs_debit
                        "unit_amount": 2000,
                        "product_data": {
                            "name": "Sample Product Name",
                            "images": ["https://i.imgur.com/EHyR2nP.png"],
                            "description": "Sample Description",
                        },
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
            metadata=metadata,
        )

        context["CHECKOUT_SESSION_ID"] = session.id

####
## 4. 

class PurchaseSubscriptionView(FormView):
    """
    Example view to demonstrate how to use dj-stripe to:
    * create a Customer
    * add a card to the Customer
    * create a Subscription using that card
    This does a non-logged in purchase for the user of the provided email
    """

    template_name = "purchase_subscription.html"





class CheckoutSessionSuccessView(TemplateView):

    template_name = "checkout_success.html"
    form_class = PurchaseSubscriptionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if djstripe.models.Plan.objects.count() == 0:
            raise Exception(
                "No Product Plans in the dj-stripe database - create some in your "
                "stripe account and then "
                "run `./manage.py djstripe_sync_plans_from_stripe` "
                "(or use the dj-stripe webhooks)"
            )

        context["STRIPE_PUBLIC_KEY"] = djstripe_settings.STRIPE_PUBLIC_KEY

        return context


    def form_valid(self, form):
        stripe_source = form.cleaned_data["stripe_source"]
        email = form.cleaned_data["email"]
        plan = form.cleaned_data["plan"]

        # Guest checkout with the provided email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create(username=email, email=email)

        # Create the stripe Customer, by default subscriber Model is User,
        # this can be overridden with djstripe_settings.DJSTRIPE_SUBSCRIBER_MODEL
        customer, created = djstripe.models.Customer.get_or_create(subscriber=user)

        # Add the source as the customer's default card
        customer.add_card(stripe_source)

        # Using the Stripe API, create a subscription for this customer,
        # using the customer's default payment source
        stripe_subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{"plan": plan.id}],
            collection_method="charge_automatically",
            tax_percent=19,
            api_key=djstripe.settings.STRIPE_SECRET_KEY,
        )

        # Sync the Stripe API return data to the database,
        # this way we don't need to wait for a webhook-triggered sync
        subscription = djstripe.models.Subscription.sync_from_stripe_data(
            stripe_subscription
        )

        self.request.subscription = subscription

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "djstripe_example:purchase_subscription_success",
            kwargs={"id": self.request.subscription.id},
        )



class PurchaseSubscriptionSuccessView(DetailView):
    template_name = "purchase_subscription_success.html"

    queryset = djstripe.models.Subscription.objects.all()
    slug_field = "id"
    slug_url_kwarg = "id"
    context_object_name = "subscription"


def create_payment_intent(request):
    if request.method == "POST":
        intent = None
        data = json.loads(request.body)
        try:
            if "payment_method_id" in data:
                # Create the PaymentIntent
                intent = stripe.PaymentIntent.create(
                    payment_method=data["payment_method_id"],
                    amount=1099,
                    currency="usd",
                    confirmation_method="manual",
                    confirm=True,
                    api_key=settings.STRIPE_SECRET_KEY,
                )
            elif "payment_intent_id" in data:
                intent = stripe.PaymentIntent.confirm(
                    data["payment_intent_id"],
                    api_key=settings.STRIPE_SECRET_KEY,
                )
        except stripe.error.CardError as e:
            # Display error on client
            return_data = json.dumps({"error": e.user_message}), 200
            return HttpResponse(
                return_data[0], content_type="application/json", status=return_data[1]
            )

        if (
            intent.status == "requires_action"
            and intent.next_action.type == "use_stripe_sdk"
        ):
            # Tell the client to handle the action
            return_data = (
                json.dumps(
                    {
                        "requires_action": True,
                        "payment_intent_client_secret": intent.client_secret,
                    }
                ),
                200,
            )
        elif intent.status == "succeeded":
            # The payment did not need any additional actions and completed!
            # Handle post-payment fulfillment
            return_data = json.dumps({"success": True}), 200
        else:
            # Invalid status
            return_data = json.dumps({"error": "Invalid PaymentIntent status"}), 500
        return HttpResponse(
            return_data[0], content_type="application/json", status=return_data[1]
        )

    else:
        ctx = {"STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY}
        return TemplateResponse(request, "payment_intent.html", ctx)















# def store_test(request):
#     products = Product.objects.all()
#     context = {}
#     #customer_id = Customer.objects.get(id=1)
#     #context['customer_id'] = customer_id
#     context['products'] = products

#     return render(request, '../templates/store_test.html', context)

# def payment_sepa(request):
#     context = {}
#     return render(request, '../templates/sepa.html', context)



# @login_required
# def create_checkout_session(request: HttpRequest):
 
#     customer = Customer.objects.create() # get customer model based off request.user
 
#     if request.method == 'POST':
 
#         # Assign product price_id, to support multiple products you 
#         # can include a product indicator in the incoming POST data
#         price_id = ... # 
 
#         # Set Stripe API key
#         stripe.api_key = settings.STRIPE_SECRET_KEY
 
#         # Create Stripe Checkout session
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=["card, sepa"],
#             mode="subscription",
#             line_items=[
#                 {
#                     "price": price_id,
#                     "quantity": 1
#                 }
#             ],
#             customer=customer.id,
#             success_url=f"https://YOURDOMAIN.com/payment/success?sessid={{CHECKOUT_SESSION_ID}}",
#             cancel_url=f"https://YOURDOMAIN.com/payment/cancel", # The cancel_url is typically set to the original product page
#         )
 
#     return JsonResponse({'sessionId': checkout_session['id']})







# def checkout(request):
#   products = Product.objects.all()
#   return render(request,"checkout.html",{"products": products})





# @login_required
# def create_sub(request):
#   if request.method == 'POST':
#       # Reads application/json and returns a response
#       data = json.loads(request.body)
#       payment_method = data['payment_method']
#       stripe.api_key = settings.STRIPE_SECRET_KEY

#       payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
#       djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)


#       try:
#           # This creates a new Customer and attaches the PaymentMethod in one API call.
#           customer = stripe.Customer.create(
#               payment_method=payment_method,
#               email=request.user
#               invoice_settings={
#                   'default_payment_method': payment_method
#               }
#           )

#           djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(customer)
#           request.user.customer = djstripe_customer
         

#           # At this point, associate the ID of the Customer object with your
#           # own internal representation of a customer, if you have one.
#           # print(customer)

#           # Subscribe the user to the subscription created
#           subscription = stripe.Subscription.create(
#               customer=customer.id,
#               items=[
#                   {
#                       "price": data["price_id"],
#                   },
#               ],
#               expand=["latest_invoice.payment_intent"]
#           )

#           djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(subscription)

#           request.user.subscription = djstripe_subscription
#           request.user.save()

#           return JsonResponse(subscription)
#       except Exception as e:
#           return JsonResponse({'error': (e.args[0])}, status =403)
#   else:
#     return HttpResponse('requet method not allowed')

# def complete(request):
#     return render(request, "complete.html")