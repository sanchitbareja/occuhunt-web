from django.contrib import admin
from applications.models import Application

#register the admin site

class ApplicationAdmin(admin.ModelAdmin):
	list_display = ['id','user','company','fair','status','position','note','timestamp']

admin.site.register(Application,ApplicationAdmin)
