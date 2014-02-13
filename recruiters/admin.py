from django.contrib import admin
from recruiters.models import CompanyRecruiter

#register the admin site

class CompanyRecruiterAdmin(admin.ModelAdmin):
	list_display = ['id','company','recruiter']

admin.site.register(CompanyRecruiter, CompanyRecruiterAdmin)