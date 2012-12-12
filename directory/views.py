from django.shortcuts import render_to_response
from django.shortcuts import render
from directory.models import *


def categories(request):
    rootNodes = Node.objects.filter(parent_id = 1)
    return render('directory/main.html', {'rootNodes': rootNodes})

def root(request):
    rootNodes = Node.objects.filter(parent_id = 1)
    return render('directory/main.html', {'rootNodes': rootNodes})
