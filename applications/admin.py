from django.contrib import admin
from applications.models import Application, Note

#register the admin site

class ApplicationAdmin(admin.ModelAdmin):
	list_display = ['id','user','company','fair','status','position','timestamp']

admin.site.register(Application,ApplicationAdmin)

class NoteAdmin(admin.ModelAdmin):
	list_display = ['id','user','recruiter','note','timestamp']

admin.site.register(Note,NoteAdmin)
