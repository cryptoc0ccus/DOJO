from django.shortcuts import render
from .models import *




# Create your views here.
# import qrcode
# import qrcode.image.svg
# from io import BytesIO

def createqrcode(request):
    name ="welcome to"
    obj = Member.objects.get(id=1)

    context = {
        'name': name,
        'obj': obj,
    }

    return render(request, 'member_qrcode.html', context )

#     context = {}
#     if request.method == "POST":
#         factory = qrcode.image.svg.SvgImage

def rendertesthash(request, pk):
    testhash_id = TestHash.objects.get(id=pk)
    context = {'testhash': testhash_id}

    return render(request, 'testhash.html', context )
