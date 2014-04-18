from django.conf.urls import patterns, include, url
from users.views import verify_user_network, get_user_network
from companies.views import home, splash, companies, company, search
from resumes.views import resume_feed, sign_s3_upload, submit_resume, individual_resume
from jobs.views import favorites, apply_jobs, match_jobs
from recommendations.views import recommendation_main, recommendation_new, recommendation_new_with_request, recommendation_requests, recommendation_requests_new, showcase_notifications, showcase_applications
from fairs.views import create_fair, all_events, career_fair_handler, infosession_handler, three_five_seven_handler, StartupCareerFairSpring2014View, ISchoolInfoCampView, PBLCareerFairSpring2014View, Dropin357View, Dropin3572View, Dropin3573View, GestureKitInfosession15April2014View
from recruiters.views import recruiter_splash, recruiter_hire, recruiter_market, recruiter_sell, recruiter_sponsorship_request, download_pdf, recruiter_login, recruiter_login_third_party, recruiter_analytics, download_excel_to_export
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# API
from tastypie.api import Api
from api.api import FairResource, RoomResource, CompanyResource, FavoriteResource, UserResource, ResumeResource, CommentResource, RecommendationRequestResource, RecommendationResource, HuntResource, ApplicationResource, JobResource
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
v1_api.register(JobResource())

# API
from tastypie.api import Api
from api.apiv2 import CompanyResource, UserResource, FairResource, FavoriteResource, HuntResource, JobResource, NotificationResource, CommentResource, ResumeResource, ApplicationResource
from api.views import logout_view, login_error, feedback_form

v2_api = Api(api_name='v2')
v2_api.register(CompanyResource())
v2_api.register(UserResource())
v2_api.register(FairResource())
v2_api.register(FavoriteResource())
v2_api.register(HuntResource())
v2_api.register(JobResource())
v2_api.register(NotificationResource())
v2_api.register(CommentResource())
v2_api.register(ResumeResource())
v2_api.register(ApplicationResource())

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
    url(r'^showcase/new/([A-Za-z0-9_-]+)/$', recommendation_new, name='recommendation_new'),
    url(r'^showcase/new/([A-Za-z0-9_-]+)/request/([A-Za-z0-9_-]+)/$', recommendation_new_with_request, name='recommendation_new_with_request'),
    url(r'^showcase/requests/$', recommendation_requests, name='recommendation_requests'),
    url(r'^showcase/requests/new/$', recommendation_requests_new, name='recommendation_requests_new'),
    url(r'^showcase/analytics/$', showcase_notifications, name='showcase_notifications'),
    url(r'^showcase/applications/$', showcase_applications, name='showcase_applications'),
    url(r'^match/$', match_jobs, name='match'),
    url(r'^apply/$', apply_jobs, name='apply'),
    url(r'^recruiter/$', recruiter_splash, name='recruiter_splash'),
    url(r'^recruiter/login/$', recruiter_login, name='recruiter_login'),
    url(r'^recruiter/login/third_party/$', recruiter_login_third_party, name='recruiter_login_third_party'),
    url(r'^recruiter/change-password/$', 'django.contrib.auth.views.password_change', {'template_name': 'registeration/password_change_form.html'}),
    url(r'^recruiter/change-password-success/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'registeration/password_change_done.html'}),
    url(r'^recruiter/hire/$', recruiter_hire, name='recruiter_hire'),
    url(r'^recruiter/hire/download_excel_to_export/$', download_excel_to_export, name='download_excel_to_export'),
    url(r'^recruiter/analytics/$', recruiter_analytics, name='recruiter_analytics'),
    url(r'^recruiter/candidate/download_pdf/$',download_pdf),
    url(r'^recruiter/market/$', recruiter_market, name='recruiter_market'),
    url(r'^recruiter/sell/$', recruiter_sell, name='recruiter_sell'),
    url(r'^recruiter/sponsorship-request/$', recruiter_sponsorship_request, name='recruiter_sponsorship_request'),
    url(r'^feedback/$',feedback_form),
    url(r'^privacy/$',TemplateView.as_view(template_name="privacy_policy.html")),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^login-error/$', login_error, name='login-error'),

    # Career Fairs
    url(r'^fair/UCBerkeley/Just-In-Time-Job-Fair-Spring-2014/$', TemplateView.as_view(template_name="CareerFairs/UCBerkeley/JustInTimeJobFairSpring2014.html")),
    url(r'^fair/UCBerkeley/PBL-Career-Fair-Spring-2014/$', PBLCareerFairSpring2014View, name='PBL-Career-Fair-Spring-2014'),
    url(r'^fair/UCBerkeley/CED-Career-Fair-Spring-2014/$', TemplateView.as_view(template_name="CareerFairs/UCBerkeley/CEDFairSpring2014.html")),
    url(r'^fair/UCBerkeley/InfoCamp-iSchool-Spring-2014/$', ISchoolInfoCampView, name='ISchool-InfoCamp'),
    url(r'^fair/UCBerkeley/Energy-Environment-Natural-Resources-Career-Fair-Spring-2014/$', TemplateView.as_view(template_name="CareerFairs/UCBerkeley/EnergyEnvironmentNaturalResourcesCareerFairSpring2014.html")),
    url(r'^fair/UCBerkeley/Startup-Fair-Spring-2014/$', StartupCareerFairSpring2014View, name='Startup-Fair-Spring-2014'),
    url(r'^fair/UCBerkeley/Internship-Summer-Fair-Spring-2014/$', TemplateView.as_view(template_name="CareerFairs/UCBerkeley/InternshipSummerFairSpring2014.html")),
    url(r'^fair/UCBerkeley/Spring-Career-Fair-Spring-2014/$', TemplateView.as_view(template_name="CareerFairs/UCBerkeley/SpringCareerFairSpring2014.html")),
    url(r'^fair/UCBerkeley/EECS-Internship-Fair-Spring-2014/$', TemplateView.as_view(template_name="CareerFairs/UCBerkeley/EECSInternshipOpenHouseSpring2014.html")),
    url(r'^fair/UCBerkeley/Civil-Environmental-Fair-Fall-2013/$', TemplateView.as_view(template_name="CareerFairs/UCBerkeley/CivilAndEnvironmentalEngineeringCareerFairFall2013.html")),
    url(r'^fair/UCBerkeley/Early-Bird-Internship-Fair-Fall-2013/$', TemplateView.as_view(template_name="CareerFairs/UCBerkeley/EarlyBirdInternshipFairFall2013.html")),
    url(r'^fair/UCBerkeley/Startup-Fair-Fall-2013/$', TemplateView.as_view(template_name="CareerFairs/UCBerkeley/StartupCareerFairFall2013.html")),
    url(r'^fair/UCBerkeley/EECS-Fair-Fall-2013/$', TemplateView.as_view(template_name="CareerFairs/UCBerkeley/EECSCareerFairFall2013.html")),

    # Dropins
    url(r'^fair/UCBerkeley/357-Dropin-April-9-2014/$', Dropin357View, name='357-Dropin-April-9-2014'),
    url(r'^fair/UCBerkeley/357-Dropin-April-16-2014/$', Dropin3572View, name='357-Dropin-April-16-2014'),
    url(r'^fair/UCBerkeley/357-Dropin-April-23-2014/$', Dropin3573View, name='357-Dropin-April-23-2014'),

    # Infosessions
    url(r'^fair/UCBerkeley/GestureKit-Infosession-April-15-2014/$', GestureKitInfosession15April2014View, name='GestureKit-Infosession-April-15-2014'),

    url(r'^static/faircoords/1_1.json', RedirectView.as_view(url='https://occuhuntstatic.s3.amazonaws.com/faircoords/1_1.json')),
    url(r'^static/faircoords/2_2.json', RedirectView.as_view(url='https://occuhuntstatic.s3.amazonaws.com/faircoords/2_2.json')),
    url(r'^static/faircoords/2_3.json', RedirectView.as_view(url='https://occuhuntstatic.s3.amazonaws.com/faircoords/2_3.json')),
    url(r'^static/faircoords/2_4.json', RedirectView.as_view(url='https://occuhuntstatic.s3.amazonaws.com/faircoords/2_4.json')),
    url(r'^static/faircoords/3_1.json', RedirectView.as_view(url='https://occuhuntstatic.s3.amazonaws.com/faircoords/3_1.json')),
    url(r'^static/faircoords/4_2.json', RedirectView.as_view(url='https://occuhuntstatic.s3.amazonaws.com/faircoords/4_2.json')),
    url(r'^static/faircoords/4_3.json', RedirectView.as_view(url='https://occuhuntstatic.s3.amazonaws.com/faircoords/4_3.json')),
    url(r'^static/faircoords/4_4.json', RedirectView.as_view(url='https://occuhuntstatic.s3.amazonaws.com/faircoords/4_4.json')),
    url(r'^static/faircoords/5_2.json', RedirectView.as_view(url='https://occuhuntstatic.s3.amazonaws.com/faircoords/5_2.json')),
    url(r'^static/faircoords/5_3.json', RedirectView.as_view(url='https://occuhuntstatic.s3.amazonaws.com/faircoords/5_3.json')),
    url(r'^static/faircoords/5_4.json', RedirectView.as_view(url='https://occuhuntstatic.s3.amazonaws.com/faircoords/5_4.json')),
    url(r'^static/faircoords/6_1.json', RedirectView.as_view(url='https://occuhuntstatic.s3.amazonaws.com/faircoords/6_1.json')),
    url(r'^static/faircoords/7_1.json', RedirectView.as_view(url='https://occuhuntstatic.s3.amazonaws.com/faircoords/7_1.json')),
    url(r'^static/faircoords/8.json', RedirectView.as_view(url='https://occuhuntstatic.s3.amazonaws.com/faircoords/8.json')),
    url(r'^static/faircoords/8_.json', RedirectView.as_view(url='https://occuhuntstatic.s3.amazonaws.com/faircoords/8_.json')),
    url(r'^static/faircoords/8_2.json', RedirectView.as_view(url='https://occuhuntstatic.s3.amazonaws.com/faircoords/8_2.json')),
    url(r'^static/faircoords/8_3.json', RedirectView.as_view(url='https://occuhuntstatic.s3.amazonaws.com/faircoords/8_3.json')),
    url(r'^static/faircoords/8_4.json', RedirectView.as_view(url='https://occuhuntstatic.s3.amazonaws.com/faircoords/8_4.json')),
    url(r'^static/faircoords/9_1.json', RedirectView.as_view(url='https://occuhuntstatic.s3.amazonaws.com/faircoords/9_1.json')),
    url(r'^static/faircoords/10_1.json', RedirectView.as_view(url='https://occuhuntstatic.s3.amazonaws.com/faircoords/10_1.json')),
    url(r'^static/faircoords/11_5.json', RedirectView.as_view(url='https://occuhuntstatic.s3.amazonaws.com/faircoords/11_5.json')),
    url(r'^static/faircoords/12_6.json', RedirectView.as_view(url='https://occuhuntstatic.s3.amazonaws.com/faircoords/12_6.json')),
    url(r'^static/faircoords/13_2.json', RedirectView.as_view(url='https://occuhuntstatic.s3.amazonaws.com/faircoords/13_2.json')),

    # Test urls
    url(r'^events/$', all_events, name='events'),
    url(r'^event-fair/([A-Za-z0-9_-]+)/([0-9]+)/', career_fair_handler, name="career_fair_handler"),
    url(r'^infosession/([A-Za-z0-9_-]+)/([0-9]+)/', infosession_handler, name="infosession_handler"),
    url(r'^357/([0-9]+)/', three_five_seven_handler, name="three_five_seven_handler"),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # social-auth-urls
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^done/$', home, name='home'),

    # confirm network
    url(r'^confirm-network/$', get_user_network, name='get-email-network'),
    url(r'^verify/(.+)/$', verify_user_network, name='verify-email-network'),
    
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^fair/create-fair/$', create_fair, name="create_fair"),

    # v1 API

    url(r'^api/', include(v1_api.urls)),
    url(r'^api/', include(v2_api.urls)),
    url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

