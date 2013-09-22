from django.contrib import admin
from hunting.models import Hunting

#register the admin site

class HuntingAdmin(admin.ModelAdmin):
	list_display = ['id','user','fair']
admin.site.register(Hunting, HuntingAdmin)
