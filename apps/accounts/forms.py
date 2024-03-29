from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Account
from apps.datatables.models import Document


class RegistrationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ("email",
                  "password1",
                  "password2")


class AccountAuthenticationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            if not authenticate(email=email, password=password):
                self.add_error("password", "E-Mail or Password are wrong.")
                raise forms.ValidationError('E-Mail or Password are wrong.')


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ()

class UploadDocumentForm(forms.ModelForm):

    class Meta:
        widgets = {'student': forms.HiddenInput()}
        model = Document
        fields = '__all__'
       