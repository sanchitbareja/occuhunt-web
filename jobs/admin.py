from django.contrib import admin
from jobs.models import Job, JobRanking

#register the admin site

class JobAdmin(admin.ModelAdmin):
	list_display = ['id','name','job_type','location']

class JobRankingAdmin(admin.ModelAdmin):
	list_display = ['id','job','user','category','notes']

admin.site.register(Job, JobAdmin)
admin.site.register(JobRanking, JobRankingAdmin)
