from django.conf.urls import patterns, include, url
from users.views import verify_user_network, get_user_network, preference_view
from companies.views import home, splash, companies, company, search, search_query
from resumes.views import resume_feed, sign_s3_upload, submit_resume, individual_resume
from jobs.views import favorites, apply_jobs, match_jobs
from notifications.views import showcase_notifications, showcase_applications
from fairs.views import create_fair, all_events, career_fair_handler, infosession_handler, three_five_seven_handler
from recruiters.views import recruiter_splash, recruiter_hire, recruiter_market, recruiter_sell, recruiter_sponsorship_request, download_pdf, recruiter_login, recruiter_login_third_party, recruiter_analytics, download_excel_to_export
from offers.views import offrhunt_handler
from documents.views import dashboard_view, documents_view, preview_document
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# API
from tastypie.api import Api
from api.apiv2 import CompanyResource, UserResource, FairResource, JobResource, NotificationResource, ApplicationResource, DocumentResource, LinkResource, VisitResource, ApplicationSearchResource, OfferResource
from api.views import logout_view, login_error, feedback_form

v2_api = Api(api_name='v2')
v2_api.register(CompanyResource())
v2_api.register(UserResource())
v2_api.register(FairResource())
v2_api.register(JobResource())
v2_api.register(NotificationResource())
v2_api.register(ApplicationResource())
v2_api.register(DocumentResource())
v2_api.register(LinkResource())
v2_api.register(VisitResource())
v2_api.register(ApplicationSearchResource())
v2_api.register(OfferResource())

urlpatterns = patterns('',
    url(r'^$', splash, name='splash'),
    url(r'^company/(.+)/$', company, name='company'),
    (r'^search/', include('haystack.urls')),
    url(r'^plan/resume-feed/$', resume_feed, name="resume-feed"),
    url(r'^plan/resume-feed/(?P<hashstr>[^/]+)/$', individual_resume, name="individual-resume"),
    url(r'^plan/resume-feed/new-resume/sign_s3_upload/$', sign_s3_upload, name="sign_s3_upload"),
    url(r'^plan/resume-feed/new-resume/submit_resume/$', submit_resume, name="submit_resume"),
    # url(r'^plan/organize/$', organize_companies, name="organize"),
    url(r'^plan/companies/$', favorites, name='favorites'),
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
    url(r'^faq/$',TemplateView.as_view(template_name="faq.html")),
    url(r'^privacy/$',TemplateView.as_view(template_name="privacy_policy.html")),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^login-error/$', login_error, name='login-error'),

    # Test urls
    url(r'^events/$', dashboard_view, name='dashboard_view'),
    url(r'^event-fair/([A-Za-z0-9_-]+)/([0-9]+)/', career_fair_handler, name="career_fair_handler"),
    url(r'^infosession/([A-Za-z0-9_-]+)/([0-9]+)/', infosession_handler, name="infosession_handler"),
    url(r'^357/([0-9]+)/$', three_five_seven_handler, name="three_five_seven_handler"),
    url(r'^offrhunt/$', offrhunt_handler, name='offrhunt'),
    url(r'^profile/documents/$', documents_view, name='documents_view'),
    url(r'^profile/general/$', preference_view, name='preference_view'),
    url(r'^profile/notifications/$', showcase_notifications, name='showcase_notifications'),
    url(r'^document/([A-Za-z0-9_-]+)/([A-Za-z0-9_-]+)/$', preview_document, name='preview_document'),
    url(r'^rhomepage/$', TemplateView.as_view(template_name="recruiter/recruiter_splash2.html")),
    url(r'^search-companies/$', search_query, name='search_companies'),

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

    # v2 API
    url(r'^api/', include(v2_api.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

