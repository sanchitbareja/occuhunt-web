from django.contrib import admin
from jobs.models import Job

#register the admin site

class JobAdmin(admin.ModelAdmin):
	list_display = ['id','name','company','network','fair','job_type','location','deactivate']

admin.site.register(Job, JobAdmin)
