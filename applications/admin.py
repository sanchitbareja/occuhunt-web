from django.contrib import admin
from applications.models import ApplicationTracking, Application, ApplicationDocument

#register the admin site

class ApplicationTrackingAdmin(admin.ModelAdmin):
	list_display = ['id','user','company','status','note','added_by_user','timestamp']

class ApplicationAdmin(admin.ModelAdmin):
	list_display = ['id','application_status','user','company','fair','status','position','note','timestamp','recruiter_email','recruiter_message']

class ApplicationDocumentAdmin(admin.ModelAdmin):
	list_display = ['id','application','document']

admin.site.register(ApplicationTracking,ApplicationTrackingAdmin)
admin.site.register(Application,ApplicationAdmin)
admin.site.register(ApplicationDocument,ApplicationDocumentAdmin)