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

class AddFirm(BaseView):
	@get
	def addfirm_get(self, request):
		return HttpResponse('GET Fired!')

	@post
	def addfirm_post(self, request):
		return HttpResponse('POST Fired!')

def offerView(request, offer_id):
    rootNodes = Node.objects.filter(parent_id = 1)
    return HttpResponse('offerView!')

def firmView(request, firm_slug):
    rootNodes = Node.objects.filter(parent_id = 1)
    return HttpResponse('firmView!')

def firmOffers(request, firm_slug):
    rootNodes = Node.objects.filter(parent_id = 1)
    return HttpResponse('firmOffers!')

def firmCatOffers(request, firm_slug, cat_slug):
    rootNodes = Node.objects.filter(parent_id = 1)
    return HttpResponse('firmCatOffers!')

def catView(request, cat_slug):
    rootNodes = Node.objects.filter(parent_id = 1)
    return HttpResponse('catView!')
