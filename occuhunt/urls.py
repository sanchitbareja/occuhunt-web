from django.conf.urls import patterns, include, url
from companies.views import home, splash, companies, company, search
from resumes.views import resume_feed, sign_s3_upload, submit_resume, individual_resume
from jobs.views import favorites, apply_jobs, match_jobs
from recommendations.views import recommendation_main, recommendation_new, recommendation_requests, recommendation_requests_new
from fairs.views import create_fair
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# API
from tastypie.api import Api
from api.api import CompanyResource, FavoriteResource, UserResource, ResumeResource, CommentResource, RecommendationRequestResource, RecommendationResource
from api.views import logout_view, login_error, feedback_form

v1_api = Api(api_name='v1')
v1_api.register(CompanyResource())
v1_api.register(FavoriteResource())
v1_api.register(UserResource())
v1_api.register(ResumeResource())
v1_api.register(CommentResource())
v1_api.register(RecommendationRequestResource())
v1_api.register(RecommendationResource())

urlpatterns = patterns('',
    url(r'^home/$', home, name='home'),
    url(r'^$', splash, name='splash'),
    url(r'^company/(.+)/$', company, name='company'),
    url(r'^search/$', search, name='search'),
    url(r'^plan/resume-feed/$', resume_feed, name="resume-feed"),
    url(r'^plan/resume-feed/(?P<hashstr>[^/]+)/$', individual_resume, name="individual-resume"),
    url(r'^plan/resume-feed/new-resume/sign_s3_upload/$', sign_s3_upload, name="sign_s3_upload"),
    url(r'^plan/resume-feed/new-resume/submit_resume/$', submit_resume, name="submit_resume"),
    # url(r'^plan/organize/$', organize_companies, name="organize"),
    url(r'^plan/companies/$', favorites, name='favorites'),
    url(r'^recommend/$', recommendation_main, name='recommendation_main'),
    url(r'^recommend/new/(.+)/$', recommendation_new, name='recommendation_new'),
    url(r'^recommend/requests/$', recommendation_requests, name='recommendation_requests'),
    url(r'^recommend/requests/new/$', recommendation_requests_new, name='recommendation_requests_new'),
    url(r'^match/$', match_jobs, name='match'),
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

    url(r'^fair/create-fair/$', create_fair, name="create_fair"),

    # v1 API
    url(r'^api/', include(v1_api.urls)),
    url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

