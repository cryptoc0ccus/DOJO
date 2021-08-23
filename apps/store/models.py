from django.db import models




class StripeSubscription(models.Model):
    start_date = models.DateTimeField(help_text="The start date of the subscription.")
    status = models.CharField(max_length=20, help_text="The status of this subscription.")
    # other data we need about the Subscription from Stripe goes here 


class MyStripeModel(models.Model):
    name = models.CharField(max_length=100)
    stripe_subscription = models.ForeignKey(StripeSubscription, on_delete=models.CASCADE)


