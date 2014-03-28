from django.contrib import admin
from fairs.models import Event, Fair, Room, Map, Table, Fitting

#register the admin site
class FittingAdmin(admin.ModelAdmin):
	list_display = ['id','x1','y1','x2','y2','fn','label','image']
admin.site.register(Fitting, FittingAdmin)

class TableAdmin(admin.ModelAdmin):
	list_display = ['id','x','y','width','height','rotation','company']
admin.site.register(Table, TableAdmin)

class MapAdmin(admin.ModelAdmin):
	list_display = ['id']
admin.site.register(Map, MapAdmin)

class RoomAdmin(admin.ModelAdmin):
	list_display = ['id','name']
admin.site.register(Room, RoomAdmin)

class FairAdmin(admin.ModelAdmin):
	list_display = ['id','time_start','time_end','name','logo','venue','get_rooms']
admin.site.register(Fair, FairAdmin)

class EventAdmin(admin.ModelAdmin):
	list_display = ['id','time_start','time_end','name']
admin.site.register(Event,EventAdmin)
