from datetime import datetime, date

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
from django.contrib import messages

from DOJO import settings

# A bunch of variables
plan = 'pioneer'
coupon = 'none'
price = 900
og_dollar = 90
coupon_dollar = 0
final_dollar = 90

#


#price_kids_4_weeks = 'price_1Jj3Q3JJBXKsbxPkmiRc6Q2A' # DOJO TEST

founder_price = 'price_1JlswKJJBXKsbxPkBzFO5irB'
#
pioneer_price = 'price_1JmEdoJJBXKsbxPkofBn2gV9'
#
price_kids_4_weeks  = 'price_1JdAT0JJBXKsbxPkgXetw6wR'


stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
 #'sk_test_51JR01OJJBXKsbxPkNGdWryMhrnATm1TlkNroOUoGDa91UUIo5RvCIY7I6PMYQgRxFWnrLYHRksHwBJYUh43EcBww00wCQ8y8Sa'#'pk_test_51JR01OJJBXKsbxPkPwpPtbUyxf9k394RCe8glAcLPNtbqvcFW23DERkkTJMNQy6bCVpNyD29rQThQDCtYv8eiLjW00LwbbBC29'

# User needs to agree with terms before moving on

def terms(request):
    student = request.user.student
    price_age = 'adult'
    if student.is_teen:
        price_age = 'teen'

    if student.is_kid:
        price_age = 'kid'
    
    print(price_age)
 
    return render(request, 'terms.html', {'student' :student, 'price_age': price_age})

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
    
    student = request.user.student
    price_age = 'adult'    
    premium = 'yes'
    founder = 'no'

    if student.is_teen:
        price_age = 'teen'

    if student.is_kid:
        price_age = 'kid'
    
    if student.is_founder:
        founder = 'founder'
    
    if student.membership.activation_counter != 0:
        premium = 'no'
    
    context = {'data': data, 'student': student, 'price_age' :price_age, 'founder' :founder, 'premium': premium}

    return render(request, 'join.html', context)

# SEPA

def checkout_sepa(request):
    global plan, coupon, price, og_dollar, coupon_dollar, final_dollar

    coupons = {'welcome':10, 'cheema':50, 'founder': 33}

    student = request.user.student
    price_age = 'adult'
    founder = ''

    if student.is_teen:
        price_age = 'teen'

    if student.is_kid:
        price_age = 'kid'

    try:
        if request.user.customer.membership:
            return redirect('subscription:subscription')
    except Customer.DoesNotExist:
        pass

    coupons = {'welcome':10, 'cheema':50, 'founder': 33}


    if request.method == 'POST':
        

       ################## Contracts: LATER HERE ###############################
  
       ##################### No contract ########################

        if request.POST['plan'] == 'founder':
            plan = founder_price

        if request.POST['plan'] == 'pioneer':
            plan = pioneer_price       
    


       ###################### KIDS #############################     

        if request.POST['plan'] == 'kids 4 weeks':
            plan = price_kids_4_weeks

        try:
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
                    coupon = stripe.Coupon.create(duration='forever', id=request.POST['coupon'].lower(), percent_off=percentage)
                except:
                    pass
                subscription = stripe.Subscription.create(customer=stripe_customer_sepa.id, items=[{'plan':plan}], coupon=request.POST['coupon'].lower())

            else:
                subscription = stripe.Subscription.create(customer=stripe_customer_sepa.id, items=[{'plan':plan}])

       
            customer = Customer()
            customer.user = request.user
            customer.stripeid = stripe_customer_sepa.id
       
            if subscription is not None:
                
                cust = dict(request.POST)

                str1 = cust['plan']
                remove = '[\'\']'
                str1 = str(str1)
                translation = str.maketrans('', '', remove)
                str1 = str1.translate(translation).title()
                customer.plan = str1
                start_date = datetime.fromtimestamp(subscription["current_period_start"])
                end_date = datetime.fromtimestamp(subscription["current_period_end"])
                print(start_date)
                print(end_date)



            

            customer.membership = True
            customer.cancel_at_period_end = False
            customer.stripe_subscription_id = subscription.id
            customer.last4 = source.sepa_debit.last4
            customer.mandate_ref = source.sepa_debit.mandate_reference
            
            customer.save()
            print('here', customer)
            print('here', customer.user.id)
            print('here', customer.id)
            #Update membership class
            customer.user.student.membership.is_active = True
            customer.user.student.membership.autorenew_membership = True
    #    customer.user.student.membership.activation_date = date.today()
            customer.user.student.membership.expiry_date = end_date
            customer.user.student.membership.save_timestamp()
            customer.user.student.membership.save()
        #customer.user.student.save_qrcode()

        
        #return redirect('core:index')
            return redirect('datatables:Student', customer.user.student.id)# TEST HERE
        except:
            messages.warning(request, "Invalid Name or IBAN number, Please enter Again!")
            plan = 'pioneer'
            coupon = 'none'
            price = 9000
            og_dollar = 90
            coupon_dollar = 0
            final_dollar = 90
            if request.method == 'POST' and 'plan' in request.POST:
                if request.POST['plan'] == 'adults 26 weeks':
                    plan = 'adults 26 weeks'
                    price = 60000
                    og_dollar = 600
                    final_dollar = 600
                if request.POST['plan'] == 'adults 12 weeks':
                    plan = 'adults 12 weeks'
                    price = 32400
                    og_dollar = 324
                    final_dollar = 324
                if request.POST['plan'] == 'adults 4 weeks':
                    plan = 'adults 4 weeks'
                    price = 12000
                    og_dollar = 120
                    final_dollar = 120

       ##################### No contract ########################
                if request.POST['plan'] == 'founder':                    
                    plan = founder_price
                    price = 6000
                    og_dollar = 60
                    final_dollar = 60

                if request.POST['plan'] == 'pioneer':                    
                    plan = pioneer_price
                    price = 9000
                    og_dollar = 90
                    final_dollar = 90
    ##############################################################

                if request.POST['plan'] == 'kids 52 weeks':
                    plan = 'kids 52 weeks'
                    price = 51800
                    og_dollar = 518
                    final_dollar = 518
                if request.POST['plan'] == 'kids 26 weeks':
                    plan = 'kids 26 weeks'
                    price = 29400
                    og_dollar = 294
                    final_dollar = 294
                if request.POST['plan'] == 'kids 12 weeks':
                    plan = 'kids 12 weeks'
                    price = 16500
                    og_dollar = 165
                    final_dollar = 165
                if request.POST['plan'] == 'kids 4 weeks':
                    plan = 'kids 4 weeks'
                    price = 6480
                    og_dollar = 64.8
                    final_dollar = 64.8
        
            if request.method == 'POST' and 'coupon' in request.POST:
                if request.POST['coupon'].lower() in coupons:
                    coupon = request.POST['coupon'].lower()
                    percentage = coupons[coupon]
                    coupon_price = int((percentage / 100) * price)
                    price -= coupon_price
                    coupon_dollar = str(coupon_price)[:-2] + "." + str(coupon_price)[-2:]
                    final_dollar = str(price)[:-2] + "." + str(price)[-2:]
            return render(request, 'checkout_sepa.html', {'price_age' :price_age, 'student' :student, 'plan':plan, 'coupon':coupon, 'price':price, 'og_dollar':og_dollar, 'coupon_dollar':coupon_dollar, 'final_dollar':final_dollar})



    
    else:
        
        plan = 'pioneer'
        coupon = 'none'
        price = 900
        og_dollar = 90
        coupon_dollar = 0
        final_dollar = 90
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



       ##################### No contract ########################

            if request.GET['plan'] == 'founder':
                plan = 'founder'               
                price = 6000
                og_dollar = 60
                final_dollar = 60

            if request.GET['plan'] == 'pioneer':
                plan = 'pioneer'                
                price = 9000
                og_dollar = 90
                final_dollar = 90

        ########################################################

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
        return render(request, 'checkout_sepa.html', {'price_age' :price_age, 'student' :student, 'plan':plan, 'coupon':coupon, 'price':price, 'og_dollar':og_dollar, 'coupon_dollar':coupon_dollar, 'final_dollar':final_dollar})






import json
def subscription(request):
     

    customerdata = {}
    membership = False
    cancel_at_period_end = False
 

    if request.method == 'POST':
        # Here is Cancel Membership.
        subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)
        subscription.cancel_at_period_end = True
        request.user.customer.cancel_at_period_end = True
        request.user.student.membership.autorenew_membership = False
        request.user.student.membership.save()

       
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

    
    subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)
   
    start_date = datetime.fromtimestamp(subscription["current_period_start"])
    end_date = datetime.fromtimestamp(subscription["current_period_end"])
    status = subscription['status']


    auto_renew = ''
    if cancel_at_period_end == False:
        auto_renew = 'YES'
    else:
        auto_renew = 'NO'

    
    invoice = stripe.Invoice.list(customer=request.user.customer.stripeid)


    return render(request, 'subscription.html', {'membership':membership, 'cancel_at_period_end':cancel_at_period_end,
                 'customerdata':customerdata, 'start_date' :start_date, 'end_date' :end_date, 'status' :status, 'auto_renew' :auto_renew,
                 'invoice' :invoice})

