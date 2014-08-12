from django.contrib import admin
from offers.models import Offer

#register the admin site

class OfferAdmin(admin.ModelAdmin):
	list_display = ['id','user','company_from_text','company_category','number_of_offers','salary_range','offer_deadline','offer_deadline_timestamp','interested_in_startups','interested_in_corps','companies_considering','approved','timestamp']

admin.site.register(Offer,OfferAdmin)