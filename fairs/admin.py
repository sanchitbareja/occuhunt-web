from django.contrib import admin
from fairs.models import Fair, Room

#register the admin site
class RoomAdmin(admin.ModelAdmin):
	list_display = ['id','name']
admin.site.register(Room, RoomAdmin)

class FairAdmin(admin.ModelAdmin):
	list_display = ['id','time_start','time_end','name','logo','get_rooms']
admin.site.register(Fair, FairAdmin)
