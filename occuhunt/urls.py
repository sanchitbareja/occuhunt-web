from django.conf.urls import patterns, include, url
from companies.views import home, splash, companies, company, search
from resumes.views import resume_feed, resume_feed_featured, sign_s3_upload, submit_resume
from jobs.views import favorites, apply_jobs
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# API
from tastypie.api import Api
from api.api import CompanyResource, FavoriteResource, HuntingResource, UserResource, ResumeResource, CommentResource
from api.views import logout_view, login_error, feedback_form

v1_api = Api(api_name='v1')
v1_api.register(CompanyResource())
v1_api.register(FavoriteResource())
v1_api.register(UserResource())
v1_api.register(HuntingResource())
v1_api.register(ResumeResource())
v1_api.register(CommentResource())

urlpatterns = patterns('',
    url(r'^home/$', home, name='home'),
    url(r'^$', splash, name='splash'),
    url(r'^company/(.+)/$', company, name='company'),
    url(r'^search/$', search, name='search'),
    url(r'^plan/resume-feed/$', resume_feed, name="resume-feed"),
    url(r'^plan/resume-feed/featured$', resume_feed_featured, name="resume_feed_featured"),
    url(r'^plan/resume-feed/new-resume/sign_s3_upload/$', sign_s3_upload, name="sign_s3_upload"),
    url(r'^plan/resume-feed/new-resume/submit_resume/$', submit_resume, name="submit_resume"),
    # url(r'^plan/organize/$', organize_companies, name="organize"),
    url(r'^plan/companies/$', favorites, name='favorites'),
    url(r'^apply/$', apply_jobs, name='apply'),
    url(r'^feedback/$',feedback_form),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^login-error/$', login_error, name='login-error'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # social-auth-urls
    url(r'', include('social_auth.urls')),
    url(r'^done/$', home, name='home'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # v1 API
    url(r'^api/', include(v1_api.urls)),
    url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

