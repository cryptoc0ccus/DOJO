from .models import *
from django import forms

class DateInput(forms.DateInput):
 
    input_type = 'date'



class StudentForm(forms.ModelForm):
    class Meta:
        widgets = {'birth_date': DateInput(), 'user': forms.HiddenInput()}
        model = Student
        #fields = '__all__'
        exclude = ('user',)


class GraduationForm(forms.ModelForm):
    graduation = models.OneToOneField(Student, null=True, on_delete=models.CASCADE)
    class Meta:
        widgets = {'belt_since': DateInput(), 'graduation': forms.HiddenInput()}
        model = Graduation
        fields = '__all__'


class MembershipForm(forms.ModelForm):
    class Meta:
        widgets = {'member_since': DateInput(), 'membership': forms.HiddenInput(), 'activation_date': DateInput(),}
        model = Membership
        fields = '__all__'

class PostsForm(forms.ModelForm):
    class Meta:
        widgets = {'posts': forms.HiddenInput(),'created_on': DateInput(),}
        model = Posts
        fields = '__all__'
