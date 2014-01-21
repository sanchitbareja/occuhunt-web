from django.contrib import admin
from recommendations.models import Recommendation, Request

#register the admin site

class RecommendationAdmin(admin.ModelAdmin):
	list_display = ['id','recommendation_from','recommendation_to','relationship','project','answer1','answer2','answer3','timestamp']

class RequestAdmin(admin.ModelAdmin):
	list_display = ['id', 'request_from', 'request_to', 'relationship', 'project', 'message', 'timestamp']

admin.site.register(Recommendation, RecommendationAdmin)
admin.site.register(Request, RequestAdmin)