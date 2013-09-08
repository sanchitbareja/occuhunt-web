from django.conf.urls import patterns, include, url
from companies.views import home
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# API
from tastypie.api import Api
from api.api import CompanyResource

v1_api = Api(api_name='v1')
v1_api.register(CompanyResource())

urlpatterns = patterns('',
    # Examples:
    url(r'^$', home, name='home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # social-auth-urls
    url(r'', include('social_auth.urls')),
    url(r'^done/$', home, name='home'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # v1 API
    url(r'^api/', include(v1_api.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

