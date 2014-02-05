from django.contrib import admin
from hunts.models import Hunt, Resumedrop

#register the admin site
class HuntAdmin(admin.ModelAdmin):
	list_display = ['id','user','fair']
admin.site.register(Hunt, HuntAdmin)

class ResumedropAdmin(admin.ModelAdmin):
	list_display = ['id','user','fair','company']
admin.site.register(Resumedrop, ResumedropAdmin)
