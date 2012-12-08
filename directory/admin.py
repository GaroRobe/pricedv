from directory.models import *
from django.contrib import admin

class FirmNodesInline(admin.TabularInline):
	model = FirmNodes
	extra = 0

class FirmAdmin(admin.ModelAdmin):
	inlines = [FirmNodesInline]

admin.site.register(Town)
admin.site.register(Firm, FirmAdmin)
admin.site.register(Node)
admin.site.register(Offer)