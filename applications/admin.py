from django.contrib import admin
from applications.models import Application

#register the admin site

class ApplicationAdmin(admin.ModelAdmin):
	raw_id_fields = ("documents",)
	list_display = ['id','user','company','fair','status','position','note','timestamp','recruiter_email','recruiter_message','get_documents']

admin.site.register(Application,ApplicationAdmin)
