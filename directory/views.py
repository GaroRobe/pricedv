from django.shortcuts import render_to_response
from django.shortcuts import render
from directory.models import *

import math
from httpmethod import *
from django.http import HttpResponse


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
    return render(request, 'directory/main.html', {'rootNodes': rootNodes})

class AddFirm(BaseView):
	@get
	def addfirm_get(self, request):
		return HttpResponse('GET Fired!')
	    #return render_to_response('directory/forms/addCompany.html')

	@post
	def addfirm_post(self, request):
		return HttpResponse('POST Fired!')
	    #return render_to_response('directory/forms/addCompany.html')
