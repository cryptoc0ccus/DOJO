
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin

from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect


from .models import *
from .forms import *

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

import datetime
from django.contrib import messages

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group





#render out the template
class StudentList(ListView):
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



class StudentCreate(CreateView):
    model = Student
    form_class = StudentForm
    context_object_name = 'student'
    template_name = '../templates/student_form.html'

    def get_success_url(self, **kwargs):        
        return reverse_lazy("datatables:Student", args=(self.object.pk,))

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class StudentUpdate(UpdateView):
    model = Student
    form_class = StudentForm
  #  success_url = reverse_lazy('datatables:Students')
    
    template_name = '../templates/student_form.html'

    def get_success_url(self, **kwargs):        
        messages.success(self.request, 'Student Profile updated sucessfully') 
        return reverse_lazy("datatables:Student", args=(self.object.pk,))

class StudentDelete(DeleteView):
    model = Student
    context_object_name = 'student'
    success_url = reverse_lazy('accounts:home')
    template_name = '../templates/delete.html'


## Graduation
class GraduationUpdate(UserPassesTestMixin, UpdateView):
    model = Graduation
    form_class = GraduationForm
    context_object_name = 'graduation'
    success_url = reverse_lazy('datatables:Students')
    template_name = '../templates/student_form.html'

    def test_func(self):
        return self.request.user.groups.filter(name='superuser').exists()
    
    def handle_no_permission(self):
        return redirect('accounts:home')

    

## Membership

class MembershipUpdate(UserPassesTestMixin, UpdateView):
    model = Membership
    form_class = MembershipForm
    context_object_name = 'membership'
    #success_url = reverse_lazy('datatables:Students')
    template_name = '../templates/student_form.html'

    def test_func(self):
        return self.request.user.groups.filter(name='superuser').exists()
    
    def handle_no_permission(self):
        return redirect('accounts:home')

    def get_success_url(self, **kwargs):        
        return reverse_lazy("datatables:Student", args=(self.object.student_id,))

    def form_valid(self, form):        
        self.object.save_timestamp()
        self.object = form.save()
        return super().form_valid(form)
        
class MembershipDisplay(DetailView):
    model = Membership
    context_object_name = 'membership'
    #success_url = reverse_lazy('datatables:Students')
    template_name = '../templates/membership.html'



############### Finally working - 
# FIXME: stopped working again
class PostCreate(CreateView, UserPassesTestMixin):
    model = Posts
    form_class = PostsForm
    context_object_name = 'posts'
    template_name = '../templates/student_form.html'

    def test_func(self):
        return self.request.user.groups.filter(name='superuser').exists()
    
    def handle_no_permission(self):
        return redirect('accounts:home')

    def get_success_url(self, **kwargs):        
        return reverse_lazy("datatables:Student", args=(self.object.student_id,))

    def get_context_data(self, **kwargs):
        self.student = get_object_or_404(Student, pk=self.kwargs['pk'])
        kwargs['student'] = self.student
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.student = get_object_or_404(Student, pk=self.kwargs['pk'])
        form.instance.student = self.student
        
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


class PostDelete(DeleteView, UserPassesTestMixin):
    model = Posts
    context_object_name = 'post'
   # success_url = reverse_lazy('datatables:Students')
    template_name = '../templates/delete.html'

    def test_func(self):
        return self.request.user.groups.filter(name='superuser').exists()
    
    def handle_no_permission(self):
        return redirect('accounts:home')
    
    def get_success_url(self, **kwargs):        
        return reverse_lazy("datatables:Student", args=(self.object.student_id,))

    


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
        
        return super(DocumentsCreate, self).form_valid(form)

    def get_success_url(self, **kwargs):        
        return reverse_lazy("datatables:Student", args=(self.object.student_id,))
       


class DocumentsDelete(DeleteView):
    model = Document
    context_object_name = 'docs'
    success_url = reverse_lazy('datatables:Students')
    template_name = '../templates/delete.html'



@user_passes_test(lambda u: Group.objects.get(name='superuser') in u.groups.all())
def manage_qrcode(request):
    student_id = request.GET.get('studentid')

    if request.method == 'GET': 

        if 'select' in request.GET:
            qrcodestudent = Student.objects.get(id=student_id)
            if request.GET['select'] == 'create':
                          
                qrcodestudent.save_qrcode()
                print('code is saved', qrcodestudent)
            if request.GET['select'] == 'delete':
                qrcodestudent.delete_qrcode()
                print('here we are 3')
    
            return redirect('datatables:Student', student_id)             


    return render(request, 'manage_qrcode.html', {'student' :student_id })
