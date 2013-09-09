from django.contrib import admin
from favorites.models import Favorite

#register the admin site

class FavoriteAdmin(admin.ModelAdmin):
	list_display = ['id','user','company']
admin.site.register(Favorite,FavoriteAdmin)
