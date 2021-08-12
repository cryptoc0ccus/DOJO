from django.urls.base import reverse
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy


from django.shortcuts import render

from .models import *
from .forms import *

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django_tables2 import SingleTableView
from .tables import StudentTable
# Create your views here.
from django.shortcuts import get_object_or_404

import datetime


#render out the template
class StudentList(LoginRequiredMixin, ListView):
    model = Student
    context_object_name = 'students'
    template_name = '../templates/students.html'

class StudentDetail(DetailView):
    model = Student
    context_object_name = 'student'
    template_name = '../templates/student_profile.html'

    def get_context_data(self, **kwargs):
        student = super().get_context_data(**kwargs)
        student_obj = get_object_or_404(Student,pk=self.kwargs['pk'])

        graduation = Graduation(graduation=student_obj, belt_since=datetime.date.today())
        
        student['graduation'] = graduation        
        return student

class StudentCreate(CreateView):
    model = Student
    form_class = StudentForm
    context_object_name = 'student'
    #fields = ['first_name', 'last_name']
    success_url = reverse_lazy('datatables:Students')
    template_name = '../templates/student_form.html'

class StudentUpdate(UpdateView):
    model = Student
    fields = ['first_name', 'last_name', "phone", "address"]
    success_url = reverse_lazy('datatables:Students')
    template_name = '../templates/student_form.html'

class StudentDelete(DeleteView):
    model = Student
    context_object_name = 'student'
    success_url = reverse_lazy('datatables:Students')
    template_name = '../templates/delete.html'


## Graduation
class GraduationUpdate(UpdateView):
    model = Graduation
    form_class = GraduationForm
    context_object_name = 'graduation'
    success_url = reverse_lazy('datatables:Students')
    template_name = '../templates/student_form.html'

    




# class DashboardView(View):
#     #render out the template
#     def get(self, request, *args, **kwargs):
#         students = Student.objects.all()
#         context = {'students': students}
#         return render(request, 'dashboard.html', context)

#     def post(self, request, *args, **kwargs):
#         pass









#@login_required
#@method_decorator(login_required, name='dispatch')

# class DashboardView(ListView):
#     model = Student
# def dashboard(request):
#     print('I GOT HERE')
#     return render(request, 'dashboard.html')