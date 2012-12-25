from django.shortcuts import render_to_response
from django.shortcuts import render
from directory.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
import operator

import math
from httpmethod import *
from django.http import HttpResponse
import json

def dataCounter():
    offers = Offer.objects.all().count() / 1000 * 1000
    firms = Firm.objects.all().count() / 100 * 100
    return {
        'offersAmount': offers,
        'firmsAmount': firms
    }
    
def sendEmail():
    send_mail('Subject here', 'Here is the message.', 'from@example.com',
        ['pricedv@mailforspam.com'], fail_silently=False)
    

def spreadsheet(request):
    """
    Generates an Excel spreadsheet for review by a staff member.
    """
    nodes = Node.objects.all()
    
    response = render_to_response("directory/excel.html", {
        'nodes': nodes,
    })
    filename = "nodes.xls"
    response['Content-Disposition'] = 'attachment; filename='+filename
    response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'

    return response


def categories(request):
    rootNodes = Node.objects.filter(parent_id = 1)
    return render(request, 'directory/todo.html', {'rootNodes': rootNodes})

def root(request):
    categories = Node.objects.filter(parent_id = 1)
    categoriesHalfLength = math.ceil(len(categories) / 2.0)
    townsFilter = Town.objects.exclude(offer__town_id__id__isnull=True)
    return render(request, 'directory/main.html', {
        'dataCounter': dataCounter(),
        'categories': categories,
        'townsFilter': townsFilter,
        'categoriesHalfLength': categoriesHalfLength,
    })
        
def addfirm(request):
    if request.method == 'POST': # If the form has been submitted...
        form = FirmForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            form.save()
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
    return render(request, 'directory/todo.html', {
        'firmData': firm,
    })

def firmOffers(request, firm_slug):
    firm = Firm.objects.get(slug = firm_slug)
    length = 25
    offset = 0
    offers = Offer.objects.filter(firm_id == firm.id)[:length:offset]
    return render(request, 'directory/todo.html', {
        'firmData': firm,
        'offers': offers,
    })

def firmCatOffers(request, firm_slug, cat_slug):
    firm = Firm.objects.get(slug = firm_slug)
    length = 25
    offset = 0
    offers = Offer.objects.filter(firm_id == firm.id)[:length:offset]
    return render(request, 'directory/todo.html', {
        'firmData': firm,
        'offers': offers,
    })

def catView(request, cat_slug, ):
    townsFilter = Town.objects.exclude(offer__town_id__id__isnull=True)
    category = Node.objects.get(slug = cat_slug)
    if category.parent_id.id == 1:
        #return subcategories
        subcats = Node.objects.filter(parent_id__slug = cat_slug)
        return render(request, 'directory/main.html', {
            'dataCounter': dataCounter(),
            'categories': subcats,
            'townsFilter': townsFilter,
            'categoriesHalfLength': math.ceil(len(subcats) / 2),
            'breadcrumbs': [{'url': '', 'title': category}],
        })
    else:
        pageSize = request.COOKIES.get('page-size')
        if not pageSize: pageSize = 25
        
        order = request.COOKIES.get('offers-order')
        if not order: order = "title"
        
        towns = request.GET.getlist('towns')
        filter = request.GET.getlist('filter') 

        #return offers in cat
        category_offers = Offer.objects.filter(node_id__slug = cat_slug).order_by(order)
        
        if len(towns) > 0:
            category_offers = category_offers.filter(town_id__id__in = towns )
        
        if len(filter) > 0:
            filter_crit = reduce(operator.or_, ((Q(title__contains = x)|Q(desc__contains = x)) for x in filter))
            category_offers = category_offers.filter(filter_crit)
        
        paginator = Paginator(category_offers, pageSize)

        page = request.GET.get('page')
        try:
            offers = paginator.page(page)
        except PageNotAnInteger:
            offers = paginator.page(1)
        except EmptyPage:
            offers = paginator.page(paginator.num_pages)
            
        borderPage = 4
        startPage = offers.number - borderPage
        if offers.number > paginator.num_pages - borderPage:
            startPage = startPage - paginator.num_pages + offers.number
        if startPage < 1:
            startPage = 1
            
        endPage = offers.number + borderPage
        if offers.number < borderPage:
            endPage = endPage + borderPage - startPage
        if endPage > paginator.num_pages:
            endPage = paginator.num_pages

        i = startPage
        pages = []
        while i <= endPage:
            pages.append(i)
            i = i+1
            
        return render(request, 'directory/offers.html', {
            'dataCounter': dataCounter(),
            'offers': offers,
            'townsFilter': townsFilter,
            'category': category,
            'pages': pages,
            'startPage': startPage,
            'endPage': endPage,
            'breadcrumbs': [{'url': '', 'title': category.parent_id.title}, {'url': '', 'title': category.title}],
        })

def catViewFirms(request, cat_slug, ):
    townsFilter = Town.objects.exclude(firm__town_id__id__isnull=True)
    category = Node.objects.get(slug = cat_slug)
    if category.parent_id.id == 1:
        #return subcategories
        subcats = Node.objects.filter(parent_id__slug = cat_slug)
        return render(request, 'directory/main.html', {
            'dataCounter': dataCounter(),
            'categories': subcats,
            'townsFilter': townsFilter,
            'categoriesHalfLength': math.ceil(len(subcats) / 2),
            'breadcrumbs': [{'url': '', 'title': category}],
        })
    else:
        pageSize = request.COOKIES.get('page-size')
        if not pageSize: pageSize = 25
        
        order = request.COOKIES.get('offers-order')
        if not order: order = "title"
        
        towns = request.GET.getlist('towns')
        filter = request.GET.getlist('filter') 

        #return firms in cat
        category_firms = Firm.objects.filter(firm_nodes__slug = cat_slug).distinct().order_by(order)
        
        if len(towns) > 0:
            category_firms = category_firms.filter(town_id__id__in = towns )
        
        if len(filter) > 0:
            filter_crit = reduce(operator.or_, ((Q(title__contains = x)|Q(desc__contains = x)) for x in filter))
            category_firms = category_firms.filter(filter_crit)
        
        paginator = Paginator(category_firms, pageSize)

        page = request.GET.get('page')
        try:
            firms = paginator.page(page)
        except PageNotAnInteger:
            firms = paginator.page(1)
        except EmptyPage:
            firms = paginator.page(paginator.num_pages)
            
        borderPage = 4
        startPage = firms.number - borderPage
        if firms.number > paginator.num_pages - borderPage:
            startPage = startPage - paginator.num_pages + firms.number
        if startPage < 1:
            startPage = 1
            
        endPage = firms.number + borderPage
        if firms.number < borderPage:
            endPage = endPage + borderPage - startPage
        if endPage > paginator.num_pages:
            endPage = paginator.num_pages

        i = startPage
        pages = []
        while i <= endPage:
            pages.append(i)
            i = i+1
            
        return render(request, 'directory/firms.html', {
            'dataCounter': dataCounter(),
            'firms': firms,
            'townsFilter': townsFilter,
            'category': category,
            'pages': pages,
            'startPage': startPage,
            'endPage': endPage,
            'breadcrumbs': [{'url': '', 'title': category.parent_id.title}, {'url': '', 'title': category.title}],
        })   
        
# Static pages
def about(request):
    return render(request, 'directory/todo.html')
    
