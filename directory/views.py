from django.shortcuts import render_to_response
from directory.models import *


def categories(request):
    rootNodes = Node.objects.filter(parent_id = 1)
    return render_to_response('directory/main.html', {'rootNodes': rootNodes})

def root(request):
    rootNodes = Node.objects.filter(parent_id = 1)
    return render_to_response('directory/main.html', {'rootNodes': rootNodes})

def addfirm(request):
    rootNodes = Node.objects.filter(parent_id = 1)
    return render_to_response('directory/forms/addCompany.html')
