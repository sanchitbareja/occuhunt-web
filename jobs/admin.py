from django.contrib import admin
from jobs.models import Job

#register the admin site

class JobAdmin(admin.ModelAdmin):
	list_display = ['id','name','job_type','location']

admin.site.register(Job, JobAdmin)
