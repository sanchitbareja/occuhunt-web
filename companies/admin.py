from django.contrib import admin
from companies.models import Company

#register the admin site

class CompanyAdmin(admin.ModelAdmin):
	list_display = ['name','callisto_url','website','logo','expected_hires','number_employees','number_domestic_locations','number_international_locations','company_description','job_description','position_locations','position_types']

admin.site.register(Company,CompanyAdmin)
