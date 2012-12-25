from django.conf.urls import patterns, include, url
#from directory.views import AddFirm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pricedv.views.home', name='home'),
    # url(r'^pricedv/', include('pricedv.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Static pages
    url(r'^pages/$', 'directory.views.about'),
    url(r'^pages/about/$', 'directory.views.about'),
    
    url(r'^pages/get-listed/$', 'directory.views.about'),
    
    url(r'^pages/get-listed/requirements/$', 'directory.views.about'),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     url(r'^sendEmail/$', 'directory.views.sendEmail'),
     url(r'^spreadsheet/$', 'directory.views.spreadsheet'),
     url(r'^categories/$', 'directory.views.categories'),
     url(r'^categories/firms/(?P<cat_slug>\w+)/$', 'directory.views.catViewFirms'),
     url(r'^addfirm/$', 'directory.views.addfirm'),
     url(r'^offer/(?P<offer_id>\d+)/$', 'directory.views.offerView'),
     url(r'^firms/(?P<firm_slug>\w+-\w+)/$', 'directory.views.firmView'),
     url(r'^firms/(?P<firm_slug>\w+-\w+)/fullprice/$', 'directory.views.firmOffers'),
     url(r'^firms/(?P<firm_slug>\w+-\w+)/(?P<cat_slug>\w+)/$', 'directory.views.firmCatOffers'),
     url(r'^firms/(?P<firm_slug>\w+-\w+)/\w+/(?P<cat_slug>\w+)/$', 'directory.views.firmCatOffers'),
     url(r'^(?P<cat_slug>\w+)/$', 'directory.views.catView'),
     url(r'^\w+/(?P<cat_slug>\w+)/$', 'directory.views.catView'),
     url(r'^$', 'directory.views.root'),
)