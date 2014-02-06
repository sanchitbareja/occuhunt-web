from django.contrib import admin
from hunts.models import Hunt

#register the admin site
class HuntAdmin(admin.ModelAdmin):
	list_display = ['id','user','fair']
admin.site.register(Hunt, HuntAdmin)