from django.contrib import admin
from companies.models import Company

#register the admin site

class CompanyAdmin(admin.ModelAdmin):
	search_fields = ['name','company_description','competitors']
	list_display = ['id','name','founded','funding','website','careers_website','logo','banner_image','number_employees','organization_type','company_description','competitors','avg_salary','location','intro_video']

admin.site.register(Company,CompanyAdmin)
