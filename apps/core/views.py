from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import *
from django.contrib import messages



def index(request):
    return render(request, 'index.html')

@login_required
@allowed_users(allowed_roles=['superuser', 'student'])
def dashboard(request):
    context = {}
    #get profile
    profiles = request.user.student_set.all()
    #template 
    #print(profiles..objects.get(id=))

    
    context['profiles'] = profiles
    return render(request, 'dashboard.html', context)


@login_required
@allowed_users(allowed_roles=['superuser'])
def dashboard_admin(request):
    return render(request, 'dashboard_admin.html')

