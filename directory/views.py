from django.shortcuts import render_to_response
from django.shortcuts import render
from directory.models import *

import math


def categories(request):
    rootNodes = Node.objects.filter(parent_id = 1)
    return render(request, 'directory/main.html', {'rootNodes': rootNodes})

def root(request):
    rootNodes = Node.objects.filter(parent_id = 1)
    rootNodesHalfLength = math.ceil(len(rootNodes) / 2)
    return render(request, 'directory/main.html', {
        'rootNodes': rootNodes,
        'rootNodesHalfLength': rootNodesHalfLength,
    })
