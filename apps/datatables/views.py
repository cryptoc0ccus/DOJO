from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy
from django.template import Context, Template, context


from django.shortcuts import render

from .models import *
from .forms import *

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.shortcuts import get_object_or_404

import datetime
from django.contrib import messages



#render out the template
class StudentList(LoginRequiredMixin, ListView):
    model = Student
    context_object_name = 'students'
    template_name = '../templates/students.html'

class StudentDetail(LoginRequiredMixin, DetailView):
    model = Student
    context_object_name = 'student'
    template_name = '../templates/student_profile.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_obj = get_object_or_404(Student,pk=self.kwargs['pk'])
        posts = student_obj.posts_set.all()
        docs = student_obj.document_set.all()
        context['posts'] = posts
        context['docs'] = docs


        return context

class StudentCreate(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    context_object_name = 'student'
    template_name = '../templates/student_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class StudentUpdate(LoginRequiredMixin,UpdateView):
    model = Student
    form_class = StudentForm
    success_url = reverse_lazy('datatables:Students')
    template_name = '../templates/student_form.html'

class StudentDelete(LoginRequiredMixin, DeleteView):
    model = Student
    context_object_name = 'student'
    success_url = reverse_lazy('datatables:Students')
    template_name = '../templates/delete.html'


## Graduation
class GraduationUpdate(LoginRequiredMixin,UpdateView):
    model = Graduation
    form_class = GraduationForm
    context_object_name = 'graduation'
    success_url = reverse_lazy('datatables:Students')
    template_name = '../templates/student_form.html'

    
## Membership
class MembershipUpdate(LoginRequiredMixin, UpdateView):
    model = Membership
    form_class = MembershipForm
    context_object_name = 'membership'
    #success_url = reverse_lazy('datatables:Students')
    template_name = '../templates/student_form.html'

    def get_success_url(self, **kwargs):        
        return reverse_lazy("datatables:Student", args=(self.object.membership_id,))

    def form_valid(self, form):        
        self.object.membership.membership.save_timestamp()
        self.object = form.save()
        return super().form_valid(form)
        

############### Finally working - FIXME: stopped working again
class PostCreate(CreateView):
    model = Posts
    form_class = PostsForm
    context_object_name = 'posts'
    template_name = '../templates/student_form.html'

    def get_success_url(self, **kwargs):        
        return reverse_lazy("datatables:Student", args=(self.object.student_id,))

    def get_context_data(self, **kwargs):
        self.student = get_object_or_404(Student, pk=self.kwargs['pk'])
        kwargs['student'] = self.student
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.student = get_object_or_404(Student, pk=self.kwargs['pk'])
        form.instance.student = self.student
        messages.success(self.request, 'The city has been added to the list of visited places, thank you') 
        return super().form_valid(form)

    def get_initial(self, *args, **kwargs):
        initial = super(PostCreate, self).get_initial(**kwargs)
        self.student = get_object_or_404(Student, pk=self.kwargs['pk'])
        self.student.save()
        initial['student'] = self.student # A little workaround
        return initial
 

class PostsList(ListView):
    model = Posts
    paginate_by = 3
    context_object_name = 'post_list'
    template_name = '../templates/posts_list.html'

    def get_queryset(self, **kwargs):
        return Posts.objects.filter(student_id=self.kwargs.get('pk'))


class PostDelete(DeleteView):
    model = Posts
    context_object_name = 'post'
    success_url = reverse_lazy('datatables:Students')
    template_name = '../templates/delete.html'


## Documents

class DocumentsCreate(CreateView):
    model = Document
    fields = ['file']
    template_name = '../templates/document-upload.html'
    context_object_name = 'docs'

    def dispatch(self, request, *args, **kwargs):
        return super(DocumentsCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.student = get_object_or_404(Student, pk=self.kwargs['pk'])
        form.instance.student = self.student 
        # obj = form.save(commit=False)
        # if self.request.FILES:
        #     for f in self.request.FILES.getlist('file'):
        #         obj = self.model.objects.create(file=f)

        messages.success(self.request, 'The city has been added to the list of visited places, thank you') 
        return super(DocumentsCreate, self).form_valid(form)

    def get_success_url(self, **kwargs):        
        return reverse_lazy("datatables:Student", args=(self.object.student_id,))
       


class DocumentsDelete(DeleteView):
    model = Document
    context_object_name = 'docs'
    success_url = reverse_lazy('datatables:Students')
    template_name = '../templates/delete.html'
