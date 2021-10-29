from .models import *
from django import forms

class DateInput(forms.DateInput):
 
    input_type = 'date'



class StudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].required = True



    class Meta:
        widgets = {'birth_date': DateInput(), 'user': forms.HiddenInput(), 'upload_counter': forms.HiddenInput(), 'is_ready' :forms.HiddenInput(), 'is_founder' :forms.HiddenInput() }
        model = Student
        #fields = '__all__'
        exclude = ('user', 'qr_code', 'is_kid', 'is_teen')


class GraduationForm(forms.ModelForm):
    graduation = models.OneToOneField(Student, null=True, on_delete=models.CASCADE)
    class Meta:
        widgets = {'belt_since': DateInput(), 'graduation': forms.HiddenInput()}
        model = Graduation
        fields = '__all__'


class MembershipForm(forms.ModelForm):
    class Meta:
        widgets = {'member_since': DateInput(), 'expiry_date': DateInput(), 'student': forms.HiddenInput(), }
        model = Membership
        exclude = ['activation_date', 'activation_counter']

class PostsForm(forms.ModelForm):
    class Meta:
        widgets = {'posts': forms.HiddenInput(),'created_on': DateInput(), 'student': forms.HiddenInput(), }
        model = Posts
        exclude = ('posts',)

