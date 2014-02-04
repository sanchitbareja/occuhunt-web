from django.contrib import admin
from fairs.models import Fair, Room

#register the admin site
class RoomAdmin(admin.ModelAdmin):
	list_display = ['id','name']
admin.site.register(Room, RoomAdmin)

class FairAdmin(admin.ModelAdmin):
	list_display = ['id','date_start','date_end','name','get_rooms']
admin.site.register(Fair, FairAdmin)
