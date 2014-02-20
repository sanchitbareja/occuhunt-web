from django.contrib import admin
from notifications.models import Notification

#register the admin site

class NotificationAdmin(admin.ModelAdmin):
	list_display = ['id','user','company','receiver','notification','read_receipt','timestamp']

admin.site.register(Notification,NotificationAdmin)