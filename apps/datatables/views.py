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
#    TODO: check if I still need this workaround

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_obj = get_object_or_404(Student,pk=self.kwargs['pk'])
        post = student_obj.posts_set.all()
        context['post'] = post
        t = Template("post_list.html")
        t.render(Context(context))      
        return context

class StudentCreate(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    context_object_name = 'student'
    #fields = ['first_name', 'last_name']
    #success_url = reverse_lazy('datatables:Students')
    template_name = '../templates/student_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class StudentUpdate(UpdateView):
    model = Student
    form_class = StudentForm
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

    
## Membership
class MembershipUpdate(UpdateView):
    model = Membership
    form_class = MembershipForm
    context_object_name = 'membership'
    success_url = reverse_lazy('datatables:Students')
    template_name = '../templates/student_form.html'


## Post
class PostCreate(CreateView):
    model = Posts
    form_class = PostsForm
    context_object_name = 'post'
    success_url = reverse_lazy('datatables:Students')
    template_name = '../templates/student_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_obj = get_object_or_404(Student,pk=self.kwargs['pk'])

             #student = self.post
        #print(student)
        context["post"] = post_obj.posts_set.all()
        return context



class PostDelete(DeleteView):
    model = Posts
    context_object_name = 'post'
    success_url = reverse_lazy('datatables:Students')
    template_name = '../templates/delete.html'



# def form_valid(self, form):
#         form.instance.categoria_id = self.kwargs['categoria']
#         return super().form_valid(form)


# site = Site.objects.get(id=self.kwargs['site'])
# fire_alarm.site = site

# def create_post(request, pk):
#     context = {}
#     student_id = Student.objects.get(id=pk)
#     getlink = '/students/profile/view/' + pk
#     new_post = Posts(posts=student_id, posts_created_on=datetime.date.today())

#     form = PostsForm(instance=new_post)

#     if request.method == 'POST':
#         form = PostsForm(request.POST, instance=new_post)
#         if form.is_valid():
#             form.save()

#         return redirect(getlink)
#     context['form'] = form
#     return render(request, 'cuform.html', context)


# def delete_post(request, pk):
#     post = Posts.objects.get(id=pk)
#     delete_post = 'True'
#     parent_id = post.posts.id
#     getlink = '/students/profile/view/' + str(parent_id)
#     if request.method == "POST":
#         post.delete()
#         return redirect(getlink)

#     context = {'item': post, 'delete_post': delete_post}
#     return render(request, 'delete.html', context)