from django.contrib import admin
from resumes.models import Resume, Comment

#register the admin site

class ResumeAdmin(admin.ModelAdmin):
	list_display = ['id','url','user','timestamp','anonymous','original']

class CommentAdmin(admin.ModelAdmin):
	list_display = ['id', 'x', 'y', 'resume', 'user']

admin.site.register(Resume, ResumeAdmin)
admin.site.register(Comment, CommentAdmin)
