from django.shortcuts import render_to_response
from django.shortcuts import render
from directory.models import *

import math
from httpmethod import *
from django.http import HttpResponse
import json

def categories(request):
    rootNodes = Node.objects.filter(parent_id = 1)
    return render(request, 'directory/main.html', {'rootNodes': rootNodes})

def root(request):
    categories = Node.objects.filter(parent_id = 1)
    categoriesHalfLength = math.ceil(len(categories) / 2)
    return render(request, 'directory/main.html', {
        'categories': categories,
        'categoriesHalfLength': categoriesHalfLength,
    })
		
def addfirm(request):
	if request.method == 'POST': # If the form has been submitted...
		form = FirmForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
			return HttpResponse('Validation successful: form was ("supposed to be") submitted')
		return HttpResponse('Form validation failed')
            #return HttpResponseRedirect('/thanks/') # Redirect after POST
	else:
		form = FirmForm() # An unbound form

	return render(request, 'directory/form.html', {
		'form': form,
	})

def offerView(request, offer_id):
    rootNodes = Node.objects.filter(parent_id = 1)
    return HttpResponse('offerView!')

def firmView(request, firm_slug):
	firm = Firm.objects.get(slug = firm_slug)
	return render(request, 'directory/main.html', {
		'firmData': firm,
	})

def firmOffers(request, firm_slug):
	firm = Firm.objects.get(slug = firm_slug)
	length = 50
	offset = 0
	offers = Offer.objects.filter(firm_id == firm.id)[:length:offset]
	return render(request, 'directory/main.html', {
		'firmData': firm,
		'offers': offers,
	})

def firmCatOffers(request, firm_slug, cat_slug):
	firm = Firm.objects.get(slug = firm_slug)
	length = 50
	offset = 0
	offers = Offer.objects.filter(firm_id == firm.id)[:length:offset]
	return render(request, 'directory/main.html', {
		'firmData': firm,
		'offers': offers,
	})

def catView(request, cat_slug):
	category = Node.objects.get(slug = cat_slug)
	if category.parent_id.id == 1:
		#return subcategories
		subcats = Node.objects.filter(parent_id__slug = cat_slug)
		return render(request, 'directory/main.html', {
			'categories': subcats,
			'categoriesHalfLength': math.ceil(len(subcats) / 2),
			'breadcrumbs': [{'url': '', 'title': category}],
		})
	else:
		#return offers in cat
		length = 50
		offset = 0
		offers = Offer.objects.filter(firm_id__firm_nodes__slug = cat_slug)[:length:offset]
		return render(request, 'directory/main.html', {
			'offers': offers,
			'breadcrumbs': [{'url': '', 'title': category.parent_id.title}, {'url': '', 'title': category.title}],
		})
