from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect, reverse
#from .forms import CustomSignupForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Customer, Member
from apps.datatables.models import Membership
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
import stripe
from django.http import HttpResponse

from DOJO import settings

# A bunch of variables
plan = 'adults 52 weeks'
coupon = 'none'
price = 10800
og_dollar = 1080
coupon_dollar = 0
final_dollar = 1080

#
price_adults_52_weeks = 'price_1Jd0jqJJBXKsbxPkbltSChNR'
price_adults_26_weeks = 'price_1JczxLJJBXKsbxPkCIcojgCV'
price_adults_12_weeks = 'price_1Jd9ulJJBXKsbxPkaerAUlHK'
price_adults_4_weeks  = 'price_1JdA26JJBXKsbxPkNU4wPqQc'

price_kids_52_weeks = 'price_1JdAO9JJBXKsbxPk3vMgHkb2'
price_kids_26_weeks = 'price_1JdAR5JJBXKsbxPkUTYxMr8w'
price_kids_12_weeks = 'price_1JdAS9JJBXKsbxPkIol8r3pI'
price_kids_4_weeks  = 'price_1JdAT0JJBXKsbxPkgXetw6wR'
#

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
 #'sk_test_51JR01OJJBXKsbxPkNGdWryMhrnATm1TlkNroOUoGDa91UUIo5RvCIY7I6PMYQgRxFWnrLYHRksHwBJYUh43EcBww00wCQ8y8Sa'#'pk_test_51JR01OJJBXKsbxPkPwpPtbUyxf9k394RCe8glAcLPNtbqvcFW23DERkkTJMNQy6bCVpNyD29rQThQDCtYv8eiLjW00LwbbBC29'

# User needs to agree with terms before moving on

def terms(request):
    return render(request, 'terms.html')

# User only gets the Access if membership is valid
def plan(request,pk):
    plan = get_object_or_404(Member, pk=pk)
    if plan.is_member:
        if request.user.is_authenticated:
            try:
                if request.user.customer.membership:
                        return render(request, 'plan.html', {'plan':plan})
            except Customer.DoesNotExist:
                    return redirect('terms')

        return redirect('join')
    else:
        return render(request, 'plan.html', {'plan':plan})


# Displays prices

def join(request):
    data = request.POST.get('terms')
    print(data)

    context = {'data': data}
    return render(request, 'join.html', context)

# Credit card

def checkout(request):
    
    try:
        if request.user.customer.membership:
            return redirect('subscription')
    except Customer.DoesNotExist:
        pass
        # HERE MUST BE A MODEL TO CREATE THEM CORRECTLY
    coupons = {'welcome':10, 'cheema':50}

    if request.method == 'POST':
        stripe_customer = stripe.Customer.create(email=request.user.email, source=request.POST['stripeToken'])
        plan = price_adults_52_weeks 
        
        if request.POST['plan'] == 'adults 26 weeks':
            plan = price_adults_26_weeks 

        if request.POST['plan'] == 'adults 12 weeks':
            plan = price_adults_12_weeks

        if request.POST['plan'] == 'adults 4 weeks':
            plan = price_adults_4_weeks

        if request.POST['plan'] == 'kids 52 weeks':
            plan = price_kids_52_weeks

        if request.POST['plan'] == 'kids 26 weeks':
            plan = price_kids_26_weeks

        if request.POST['plan'] == 'kids 12 weeks':
            plan = price_kids_12_weeks   

        if request.POST['plan'] == 'kids 4 weeks':
            plan = price_kids_4_weeks

        
        if request.POST['coupon'] in coupons:
            percentage = coupons[request.POST['coupon'].lower()]
            try:
                coupon = stripe.Coupon.create(duration='once', id=request.POST['coupon'].lower(), percent_off=percentage)
            except:
                pass
            subscription = stripe.Subscription.create(customer=stripe_customer.id, items=[{'plan':plan}], coupon=request.POST['coupon'].lower())

        else:
            subscription = stripe.Subscription.create(customer=stripe_customer.id, items=[{'plan':plan}])

        customer = Customer()
        customer.user = request.user
        customer.stripeid = stripe_customer.id
        customer.membership = True
        customer.cancel_at_period_end = False
        customer.stripe_subscription_id = subscription.id
        customer.save()


        #return redirect('core:index')
        return redirect('datatables:Student', customer.user.student.id)
    else:
        plan = 'adults 52 weeks'
        coupon = 'none'
        price = 108000
        og_dollar = 1080
        coupon_dollar = 0
        final_dollar = 1080
        if request.method == 'GET' and 'plan' in request.GET:
            if request.GET['plan'] == 'adults 26 weeks':
                plan = 'adults 26 weeks'
                price = 60000
                og_dollar = 600
                final_dollar = 600
            if request.GET['plan'] == 'adults 12 weeks':
                plan = 'adults 12 weeks'
                price = 32400
                og_dollar = 324
                final_dollar = 324
            if request.GET['plan'] == 'adults 4 weeks':
                plan = 'adults 4 weeks'
                price = 12000
                og_dollar = 120
                final_dollar = 120

            if request.GET['plan'] == 'kids 52 weeks':
                plan = 'kids 52 weeks'
                price = 51800
                og_dollar = 518
                final_dollar = 518
            if request.GET['plan'] == 'kids 26 weeks':
                plan = 'kids 26 weeks'
                price = 29400
                og_dollar = 294
                final_dollar = 294
            if request.GET['plan'] == 'kids 12 weeks':
                plan = 'kids 12 weeks'
                price = 16500
                og_dollar = 165
                final_dollar = 165
            if request.GET['plan'] == 'kids 4 weeks':
                plan = 'kids 4 weeks'
                price = 6480
                og_dollar = 64.8
                final_dollar = 64.8
        
        if request.method == 'GET' and 'coupon' in request.GET:
            if request.GET['coupon'].lower() in coupons:
                coupon = request.GET['coupon'].lower()
                percentage = coupons[coupon]
                coupon_price = int((percentage / 100) * price)
                price -= coupon_price
                coupon_dollar = str(coupon_price)[:-2] + "." + str(coupon_price)[-2:]
                final_dollar = str(price)[:-2] + "." + str(price)[-2:]
        return render(request, 'checkout.html', {'plan':plan, 'coupon':coupon, 'price':price, 'og_dollar':og_dollar, 'coupon_dollar':coupon_dollar, 'final_dollar':final_dollar})




def checkout_sepa(request):
    global plan, coupon, price, og_dollar, coupon_dollar, final_dollar

    coupons = {'welcome':10, 'cheema':50}

    
    try:
        if request.user.customer.membership:
            return redirect('subscription:subscription')
    except Customer.DoesNotExist:
        pass

    coupons = {'welcome':10, 'cheema':50}


    if request.method == 'POST':
        

       
        plan = price_adults_52_weeks 
        
        if request.POST['plan'] == 'adults 26 weeks':
            plan = price_adults_26_weeks 

        if request.POST['plan'] == 'adults 12 weeks':
            plan = price_adults_12_weeks

        if request.POST['plan'] == 'adults 4 weeks':
            plan = price_adults_4_weeks

        if request.POST['plan'] == 'kids 52 weeks':
            plan = price_kids_52_weeks

        if request.POST['plan'] == 'kids 26 weeks':
            plan = price_kids_26_weeks

        if request.POST['plan'] == 'kids 12 weeks':
            plan = price_kids_12_weeks   

        if request.POST['plan'] == 'kids 4 weeks':
            plan = price_kids_4_weeks


        source = stripe.Source.create(
        type='sepa_debit',
        sepa_debit={'iban': request.POST['iban']},
        currency='eur',
        owner={'name': request.POST['name'],},)

        stripe_customer_sepa = stripe.Customer.create(
                                                        email=request.user.email, 
                                                        source=source,)
        
        if request.POST['coupon'] in coupons:
            percentage = coupons[request.POST['coupon'].lower()]

            try:
                coupon = stripe.Coupon.create(duration='once', id=request.POST['coupon'].lower(), percent_off=percentage)
            except:
                pass
            subscription = stripe.Subscription.create(customer=stripe_customer_sepa.id, items=[{'plan':plan}], coupon=request.POST['coupon'].lower())

        else:
            subscription = stripe.Subscription.create(customer=stripe_customer_sepa.id, items=[{'plan':plan}])

        if subscription is not None:
            print("YAYYYYYYYYYYYY DEKHHHH", dict(request.POST))
            start_date = datetime.fromtimestamp(subscription["current_period_start"])
            end_date = datetime.fromtimestamp(subscription["current_period_end"])
            print(start_date)
            print(end_date)



        customer = Customer()
        customer.user = request.user
        customer.stripeid = stripe_customer_sepa.id
        customer.membership = True
        customer.cancel_at_period_end = False
        customer.stripe_subscription_id = subscription.id
        customer.save()
        print('here', customer)
        print('here', customer.user.id)
        print('here', customer.id)

        
        #return redirect('core:index')
        return redirect('datatables:Student', customer.user.student.id)# TEST HERE
    
    else:
        
        plan = 'adults 52 weeks'
        coupon = 'none'
        price = 108000
        og_dollar = 1080
        coupon_dollar = 0
        final_dollar = 1080
        if request.method == 'GET' and 'plan' in request.GET:
            if request.GET['plan'] == 'adults 26 weeks':
                plan = 'adults 26 weeks'
                price = 60000
                og_dollar = 600
                final_dollar = 600
            if request.GET['plan'] == 'adults 12 weeks':
                plan = 'adults 12 weeks'
                price = 32400
                og_dollar = 324
                final_dollar = 324
            if request.GET['plan'] == 'adults 4 weeks':
                plan = 'adults 4 weeks'
                price = 12000
                og_dollar = 120
                final_dollar = 120

            if request.GET['plan'] == 'kids 52 weeks':
                plan = 'kids 52 weeks'
                price = 51800
                og_dollar = 518
                final_dollar = 518
            if request.GET['plan'] == 'kids 26 weeks':
                plan = 'kids 26 weeks'
                price = 29400
                og_dollar = 294
                final_dollar = 294
            if request.GET['plan'] == 'kids 12 weeks':
                plan = 'kids 12 weeks'
                price = 16500
                og_dollar = 165
                final_dollar = 165
            if request.GET['plan'] == 'kids 4 weeks':
                plan = 'kids 4 weeks'
                price = 6480
                og_dollar = 64.8
                final_dollar = 64.8
        
        if request.method == 'GET' and 'coupon' in request.GET:
            if request.GET['coupon'].lower() in coupons:
                coupon = request.GET['coupon'].lower()
                percentage = coupons[coupon]
                coupon_price = int((percentage / 100) * price)
                price -= coupon_price
                coupon_dollar = str(coupon_price)[:-2] + "." + str(coupon_price)[-2:]
                final_dollar = str(price)[:-2] + "." + str(price)[-2:]
        return render(request, 'checkout_sepa.html', {'plan':plan, 'coupon':coupon, 'price':price, 'og_dollar':og_dollar, 'coupon_dollar':coupon_dollar, 'final_dollar':final_dollar})



def subscription(request):
     

    customerdata = {}
    membership = False
    cancel_at_period_end = False
 

    if request.method == 'POST':
        subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)
        subscription.cancel_at_period_end = True
        request.user.customer.cancel_at_period_end = True
       
        subscription.save()
        request.user.customer.save()



    else:

        try:
            if request.user.customer.membership:
                membership = True
                customerdata = request.user.customer
                


            if request.user.customer.cancel_at_period_end:
                cancel_at_period_end = True
        
        except Customer.DoesNotExist:
            membership = False

    print('here is the data: ', customerdata)
    subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)
    print('SUBSCRIPTION :', subscription)
    start_date = datetime.fromtimestamp(subscription["current_period_start"])
    end_date = datetime.fromtimestamp(subscription["current_period_end"])
    status = subscription['status']
    print(start_date)
    print(end_date)
    print(status)
    auto_renew = ''
    if cancel_at_period_end == False:
        auto_renew = 'YES'
    else:
        auto_renew = 'NO'

 
    
    return render(request, 'subscription.html', {'membership':membership, 'cancel_at_period_end':cancel_at_period_end,
                 'customerdata':customerdata, 'start_date' :start_date, 'end_date' :end_date, 'status' :status, 'auto_renew' :auto_renew})



            # print("YAYYYYYYYYYYYY DEKHHHH", dict(request.POST))
            # start_date = datetime.fromtimestamp(subscription["current_period_start"])
            # end_date = datetime.fromtimestamp(subscription["current_period_end"])
            # print(start_date)
            # print(end_date)