from django import forms

import djstripe.models


class PurchaseSubscriptionForm(forms.Form):

    email = forms.EmailField() # HERE request.user !
    plan = forms.ModelChoiceField(queryset=djstripe.models.Plan.objects.all())
    stripe_source = forms.CharField(
        max_length="255", widget=forms.HiddenInput(), required=False
    )


class PaymentIntentForm(forms.Form):
    pass