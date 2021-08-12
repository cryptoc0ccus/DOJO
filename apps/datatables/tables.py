import django_tables2 as tables
from .models import Student
from django import forms
from django_tables2.utils import A


class DateInput(forms.DateInput):
    input_type = 'date'


class StudentTable(tables.Table):
    # first_name = tables.Column()
    # last_name = tables.Column()
    age = tables.Column()
    user = tables.EmailColumn(verbose_name="E-Mail")
    action = tables.LinkColumn('people_detail', args=[A('pk')])
    
    class Meta:
        widgets = {'birth_date': DateInput()}
        model = Student
        sequence = ("first_name", "last_name", "gender", "age", "user", "phone", "action")
        exclude = ("id", "address", "profile_img", "date_created", "birth_date")
        order_by = ('first_name')
        attrs = {"class": "paleblue"}