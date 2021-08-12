from .models import *
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'


class StudentForm(forms.ModelForm):
    class Meta:
        widgets = {'birth_date': DateInput()}
        model = Student
        fields = '__all__'


class GraduationForm(forms.ModelForm):
    graduation = models.OneToOneField(Student, null=True, on_delete=models.CASCADE)
    class Meta:
        widgets = {'belt_since': DateInput(), 'graduation': forms.HiddenInput()}
        model = Graduation
        fields = '__all__'