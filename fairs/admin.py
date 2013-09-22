from django.contrib import admin
from fairs.models import Fair

#register the admin site

class FairAdmin(admin.ModelAdmin):
	list_display = ['id','venue','date_start','date_end','name']
admin.site.register(Fair, FairAdmin)
