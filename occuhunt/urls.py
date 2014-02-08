from django.conf.urls import patterns, include, url
from companies.views import home, splash, companies, company, search
from resumes.views import resume_feed, sign_s3_upload, submit_resume, individual_resume
from jobs.views import favorites, apply_jobs, match_jobs
from recommendations.views import recommendation_main, recommendation_new, recommendation_new_with_request, recommendation_requests, recommendation_requests_new, recommendation_analytics
from fairs.views import create_fair, StartupCareerFairSpring2014View
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# API
from tastypie.api import Api
from api.api import FairResource, RoomResource, CompanyResource, FavoriteResource, UserResource, ResumeResource, CommentResource, RecommendationRequestResource, RecommendationResource, HuntResource, ApplicationResource, RecruiterNotesResource
from api.views import logout_view, login_error, feedback_form

v1_api = Api(api_name='v1')
v1_api.register(CompanyResource())
v1_api.register(FavoriteResource())
v1_api.register(UserResource())
v1_api.register(ResumeResource())
v1_api.register(CommentResource())
v1_api.register(RecommendationRequestResource())
v1_api.register(RecommendationResource())
v1_api.register(RoomResource())
v1_api.register(FairResource())
v1_api.register(HuntResource())
v1_api.register(ApplicationResource())
v1_api.register(RecruiterNotesResource())

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
    url(r'^showcase/$', recommendation_main, name='recommendation_main'),
    url(r'^showcase/new/([A-Za-z0-9]+)/$', recommendation_new, name='recommendation_new'),
    url(r'^showcase/new/([A-Za-z0-9]+)/request/([A-Za-z0-9]+)/$', recommendation_new_with_request, name='recommendation_new_with_request'),
    url(r'^showcase/requests/$', recommendation_requests, name='recommendation_requests'),
    url(r'^showcase/requests/new/$', recommendation_requests_new, name='recommendation_requests_new'),
    url(r'^showcase/analytics/$', recommendation_analytics, name='recommendation_analytics'),
    url(r'^match/$', match_jobs, name='match'),
    url(r'^apply/$', apply_jobs, name='apply'),
    url(r'^feedback/$',feedback_form),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^login-error/$', login_error, name='login-error'),

    # Career Fairs
    url(r'^fair/UCBerkeley/Startup-Fair-Spring-2014/$', StartupCareerFairSpring2014View, name='Startup-Fair-Spring-2014'),
    url(r'^fair/UCBerkeley/Spring-Career-Fair-Spring-2014/$', TemplateView.as_view(template_name="CareerFairs/UCBerkeley/SpringCareerFairSpring2014.html")),
    url(r'^fair/UCBerkeley/EECS-Internship-Fair-Spring-2014/$', TemplateView.as_view(template_name="CareerFairs/UCBerkeley/EECSInternshipOpenHouseSpring2014.html")),
    url(r'^fair/UCBerkeley/Civil-Environmental-Fair-Fall-2013/$', TemplateView.as_view(template_name="CareerFairs/UCBerkeley/CivilAndEnvironmentalEngineeringCareerFairFall2013.html")),
    url(r'^fair/UCBerkeley/Early-Bird-Internship-Fair-Fall-2013/$', TemplateView.as_view(template_name="CareerFairs/UCBerkeley/EarlyBirdInternshipFairFall2013.html")),
    url(r'^fair/UCBerkeley/Startup-Fair-Fall-2013/$', TemplateView.as_view(template_name="CareerFairs/UCBerkeley/StartupCareerFairFall2013.html")),
    url(r'^fair/UCBerkeley/EECS-Fair-Fall-2013/$', TemplateView.as_view(template_name="CareerFairs/UCBerkeley/EECSCareerFairFall2013.html")),

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

