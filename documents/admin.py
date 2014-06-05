from django.contrib import admin
from documents.models import Document, Link

#register the admin site

class DocumentAdmin(admin.ModelAdmin):
	list_display = ['id','user','document_type','image_url','url','unique_hash','delete','timestamp']

class LinkAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'link_name', 'url', 'delete','timestamp']

admin.site.register(Document, DocumentAdmin)
admin.site.register(Link, LinkAdmin)
