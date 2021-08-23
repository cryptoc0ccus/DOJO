#from apps.store.models import Customer
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
#
import json
from django.http import JsonResponse
import djstripe.models
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
            reverse("djstripe_example:success")
        )

        cancel_url = self.request.build_absolute_uri(reverse("home"))






class CheckoutSessionSuccessView(TemplateView):

    template_name = "checkout_success.html"

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