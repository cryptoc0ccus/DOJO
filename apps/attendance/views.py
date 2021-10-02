from django.shortcuts import render
from .models import *

from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
# import qrcode
# import qrcode.image.svg
# from io import BytesIO

@login_required
def displayqrcode(request):
    qr_code = request.user.student.qr_code
    context = {'qr_code' :qr_code}

    return render(request, 'member_qrcode.html', context )

#     context = {}
#     if request.method == "POST":
#         factory = qrcode.image.svg.SvgImage

def rendertesthash(request, pk):
    testhash_id = TestHash.objects.get(id=pk)
    context = {'testhash': testhash_id}

    return render(request, 'testhash.html', context )
