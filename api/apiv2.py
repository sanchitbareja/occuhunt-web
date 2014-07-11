# tastypie imports
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpForbidden
from authentication import OAuth20Authentication, SessionAuthentication, RecruiterAuthentication

# imports for haystack
from django.conf.urls.defaults import *
from django.core.paginator import Paginator, InvalidPage
from tastypie.utils import trailing_slash
from django.http import Http404
from haystack.query import SearchQuerySet

# misc
from django.db.models import Q
from companies.models import Company
from favorites.models import Favorite
from fairs.models import Fair, Room, Map, Table, Fitting
from users.models import User, Major, Degree, Student, Recruiter
from applications.models import Application
from jobs.models import Job
from notifications.models import Notification
from documents.models import Document, Link, Visit
from django.contrib.sessions.models import Session
import datetime, json, random, string

class CompanyResource(ModelResource):
    class Meta:
        queryset = Company.objects.all()
        resource_name = 'companies'
        limit = 20
        authorization = DjangoAuthorization()
        authentication = SessionAuthentication()

        allowed_methods = ['get','put']
        filtering = {
            "name": ("exact"), "id": ("exact")
        }

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
        ]

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Do the query.
        sqs = SearchQuerySet().models(Company).load_all().auto_query(request.GET.get('q', ''))
        paginator = Paginator(sqs, 20)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        objects = []

        for result in page.object_list:
            bundle = self.build_bundle(obj=result.object, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'response': {'companies':objects},
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)

    def dehydrate(self, bundle):
        """
        Return a list of companies formatted according to what the developer expects
        """
        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "response"
        data['response'] = {"companies":data['objects']}
        del(data['objects'])
        return data

    def determine_format(self, request):
        return 'application/json'


class UserResource(ModelResource):    
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        authorization = DjangoAuthorization()
        authentication = SessionAuthentication()

        allowed_methods = ['get', 'put']
        filtering = {
            "first_name": ("exact"), "linkedin_uid": ("exact"),
        }
        excludes = ['password','last_login','is_active','is_admin','time_created']

    def dehydrate(self, bundle):
        """
        Return a list of users formatted according to what the developer expects
        """
        # get groups
        bundle.data['groups'] = [{'name':group.name, 'id':group.id} for group in bundle.obj.groups.all()]

        # if recruiter - return company info
        if bundle.obj.is_recruiter:
            bundle.data['company'] = {'id':bundle.obj.recruiter.company.id,
                                        'name':bundle.obj.recruiter.company.name,
                                        'founded':bundle.obj.recruiter.company.founded,
                                        'funding':bundle.obj.recruiter.company.funding,
                                        'website':bundle.obj.recruiter.company.website,
                                        'careers_website':bundle.obj.recruiter.company.careers_website,
                                        'logo':bundle.obj.recruiter.company.logo,
                                        'banner_image':bundle.obj.recruiter.company.banner_image,
                                        'number_employees':bundle.obj.recruiter.company.number_employees,
                                        'organization_type':bundle.obj.recruiter.company.organization_type,
                                        'company_description':bundle.obj.recruiter.company.company_description,
                                        'competitors':bundle.obj.recruiter.company.competitors,
                                        'avg_salary':bundle.obj.recruiter.company.avg_salary,
                                        'location':bundle.obj.recruiter.company.location,
                                        'intro_video':bundle.obj.recruiter.company.intro_video,
                                        'timestamp':bundle.obj.recruiter.company.timestamp
                                        }

        # if student - return verified email and graduation year
        if bundle.obj.is_student:
            bundle.data['student'] = {'verified_email':bundle.obj.student.verified_email,'graduation_year':bundle.obj.student.graduation_year}

        return bundle

    def obj_update(self, bundle, **kwargs):
        """
        Update user profile

        1. Expecting 

        """
        try:
            # only the user himself can update his profile - no one else
            if int(kwargs['pk']) == int(bundle.request.user.id):
                # update user preferences for Graduation Date, Major, Degree
                # update school email
                user = bundle.request.user
                # update regular email
                user = bundle.request.user
                try:
                    regular_email = bundle.data['regular_email']
                    if regular_email:
                        user.email = regular_email
                        user.save()
                except Exception, e:
                    print e
                    # raise e
                try:
                    school_email = bundle.data['school_email']
                    if school_email:
                        user.student.verified_email = school_email
                        user.student.save()
                except Exception, e:
                    print e
                    # raise e
                # update grad_year
                user = bundle.request.user
                try:
                    grad_year = bundle.data['grad_year']
                    if grad_year:
                        user.student.graduation_year = grad_year
                        user.student.save()
                except Exception, e:
                    print e
                    # raise e
                # update majors
                try:
                    majors = bundle.data['majors']
                    if majors:
                        for major in majors:
                            major_obj = Major.objects.get(id=int(major))
                            user.student.major.add(major_obj)
                        user.student.save()
                except Exception, e:
                    print e
                    # raise e
                # update degree
                try:
                    degree = Degree.objects.get(id=bundle.data['degree_type'])
                    if degree:
                        user.student.degree = degree
                        user.student.save()
                except Exception, e:
                    print e
                    # raise e

        except Exception, e:
            print e
            raise e
        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "response"
        data['response'] = {"users":data['objects']}
        del(data['objects'])
        return data

    def determine_format(self, request):
        return 'application/json'

class FairResource(ModelResource):
    organizers = fields.ManyToManyField(CompanyResource, 'organizers', full=True)
    sponsors = fields.ManyToManyField(CompanyResource, 'sponsors', full=True)

    class Meta:
        queryset = Fair.objects.all()
        resource_name = 'fairs'
        authorization = DjangoAuthorization()
        authentication = SessionAuthentication()

        allowed_methods = ['get']

    def dehydrate(self, bundle):
        """
        Return a list of fairs formatted according to what the developer expects
        """
        # get rooms
        # for each room, get a map
        # each map has tables and fittings
        # each table and fitting has their own attributes
        rooms = []
        for room in bundle.obj.rooms.all():
            room_tables = []
            room_fittings = []
            if room.map:
                for table in room.map.tables.all():
                    table_company = {'id':table.company.id,
                                        'name':table.company.name,
                                        'founded':table.company.founded,
                                        'funding':table.company.funding,
                                        'website':table.company.website,
                                        'careers_website':table.company.careers_website,
                                        'logo':table.company.logo,
                                        'banner_image':table.company.banner_image,
                                        'number_employees':table.company.number_employees,
                                        'organization_type':table.company.organization_type,
                                        'company_description':table.company.company_description,
                                        'competitors':table.company.competitors,
                                        'avg_salary':table.company.avg_salary,
                                        'location':table.company.location,
                                        'intro_video':table.company.intro_video,
                                        'timestamp':table.company.timestamp
                                        }
                    room_tables.append({'x':table.x,'y':table.y,'width':table.width,'height':table.height,'rotation':table.rotation,'company':table_company})
                for fitting in room.map.fittings.all():
                    room_fittings.append({'x1':fitting.x1,'y1':fitting.y1,'x2':fitting.x2,'y2':fitting.y2,'fn':fitting.fn,'label':fitting.label,'image':fitting.image})
                room_map = {'tables':room_tables,'fittings':room_fittings}
                room_dict = {'id':room.id,'name':room.name,'lat':room.lat,'lng':room.lng,'map':room_map}
                rooms.append(room_dict)
        bundle.data['rooms'] = rooms

        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "response"
        data['response'] = {"fairs":data['objects']}
        del(data['objects'])
        return data

    def determine_format(self, request):
        return 'application/json'

class JobResource(ModelResource):
    company = fields.OneToOneField(CompanyResource, 'company', full=True)
    class Meta:
        queryset = Job.objects.all()
        resource_name = 'jobs'
        authorization = DjangoAuthorization()
        authentication = SessionAuthentication()
        limit = 20
        always_return_data = True
        allowed_methods = ['get','post', 'put']
        filtering = {}

    def dehydrate(self, bundle):
        """
        Return a list of jobs in format as expected by developer
        """
        # get network
        # bundle.data['network'] = {'name':bundle.obj.network.name, 'id':bundle.obj.network.id}
        return bundle

    def obj_create(self, bundle, **kwargs):
        """
        Create or delete a new job
        """
        try:
            if 'deactivate' in bundle.data.keys() and bundle.data['deactivate']:
                existing_job = Job.objects.get(id=bundle.data['job_id'])
                existing_job.deactivate = True
                existing_job.save()
                bundle.obj = existing_job
            else:
                company = Company.objects.get(id=bundle.data['company_id'])
                new_job = Job(name=bundle.data['name'], job_type=bundle.data['job_type'], location=bundle.data['location'], description=bundle.data['description'], company=company)
                new_job.save()
                bundle.obj = new_job
        except Exception, e:
            print e
            raise e
        return bundle

    def obj_update(self, bundle, **kwargs):
        """
        Update to deactive mostly
        """
        try:
            if 'deactivate' in bundle.data.keys() and bundle.data['deactivate']:
                existing_job = Job.objects.get(id=bundle.data['job_id'])
                existing_job.deactivate = True
                existing_job.save()
                bundle.obj = existing_job
            else:
                company = Company.objects.get(id=bundle.data['company_id'])
                new_job = Job(name=bundle.data['name'], job_type=bundle.data['job_type'], location=bundle.data['location'], description=bundle.data['description'], company=company)
                new_job.save()
                bundle.obj = new_job
        except Exception, e:
            print e
            raise e
        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "response"
        data['response'] = {"jobs":data['objects']}
        del(data['objects'])
        return data

    def determine_format(self, request):
        return 'application/json'


class NotificationResource(ModelResource):
    user = fields.OneToOneField(UserResource, 'user', full=True)
    company = fields.OneToOneField(CompanyResource, 'company', full=True)
    class Meta:
        queryset = Notification.objects.all()
        resource_name = 'notifications'
        authorization = DjangoAuthorization()
        authentication = SessionAuthentication()
        limit = 20
        always_return_data = True
        allowed_methods = ['get','post', 'put']
        filtering = {
            "user": ("exact"), "company": ("exact"), "receiver": ("exact"), "read_receipt": ("exact")
        }

    def dehydrate(self, bundle):
        """
        Return a list of notifications in format as expected by developer
        """
        return bundle

    def obj_create(self, bundle, **kwargs):
        """
        Create or delete a new job
        """
        try:
            if 'deactivate' in bundle.data.keys() and bundle.data['deactivate']:
                existing_job = Job.objects.get(id=bundle.data['job_id'])
                existing_job.deactivate = True
                existing_job.save()
                bundle.obj = existing_job
            else:
                company = Company.objects.get(id=bundle.data['company_id'])
                new_job = Job(name=bundle.data['name'], job_type=bundle.data['job_type'], location=bundle.data['location'], description=bundle.data['description'], company=company)
                new_job.save()
                bundle.obj = new_job
        except Exception, e:
            print e
            raise e
        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "response"
        data['response'] = {"notifications":data['objects']}
        del(data['objects'])
        return data

    def determine_format(self, request):
        return 'application/json'

class DocumentResource(ModelResource):
    user = fields.OneToOneField(UserResource, 'user', full=True)
    class Meta:
        queryset = Document.objects.all().order_by('-timestamp')
        resource_name = 'documents'
        authorization = DjangoAuthorization()
        authentication = SessionAuthentication()
        limit = 20
        always_return_data = True
        allowed_methods = ['get','post','delete']
        filtering = {}

    def dehydrate(self, bundle):
        """
        Return a list of documents formatted according to what the developer expects
        """
        return bundle

    def obj_create(self, bundle, **kwargs):
        """
        Creates a new document
        """
        try:
            document_type = bundle.data['document_type']
            image_url = bundle.data['image_url']
            pdf_url = bundle.data['pdf_url']
            delete = False
            s=string.lowercase+string.digits
            unique_hash = ''.join(random.sample(s,10))
            # check if hash is indeed unique
            while Document.objects.filter(user=bundle.request.user, unique_hash=unique_hash).count() > 0:
                unique_hash = ''.join(random.sample(s,10))
            # need to check if document_url, image_url, pdf_url and delete exists
            new_doc = Document(user=bundle.request.user, document_type=document_type, image_url=image_url, url=pdf_url, unique_hash=unique_hash, delete=delete)
            new_doc.save()
            bundle.obj = new_doc
        except Exception, e:
            print e
        return bundle

    def obj_delete(self, bundle, **kwargs):
        """
        Marks a document as deleted
        """
        try:
            document = Document.objects.get(id=kwargs['pk'])
            if document.user == bundle.request.user:
                document.delete = True
                document.save()
        except Exception, e:
            print e
        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "documents"
        data['response'] = {"documents":data["objects"]}
        del(data["objects"])
        return data

    def determine_format(self, request):
        return 'application/json'


class LinkResource(ModelResource):
    user = fields.OneToOneField(UserResource, 'user', full=True)
    class Meta:
        queryset = Link.objects.all().order_by('-timestamp')
        resource_name = 'links'
        authorization = DjangoAuthorization()
        authentication = SessionAuthentication()
        limit = 20
        always_return_data = True
        allowed_methods = ['get','post','delete']
        filtering = {}

    def dehydrate(self, bundle):
        """
        Return a list of links formatted according to what the developer expects
        """
        return bundle

    def obj_create(self, bundle, **kwargs):
        """
        Creates a new link
        """
        try:
            link_label = bundle.data["label"]
            link_url = bundle.data["url"]
            delete = False
            # need to check if document_url, image_url, pdf_url and delete exists
            new_link = Link(user=bundle.request.user, link_name=link_label, url=link_url, delete=delete)
            new_link.save()
            bundle.obj = new_link
        except Exception, e:
            print e
        return bundle

    def obj_delete(self, bundle, **kwargs):
        """
        Marks a link as deleted
        """
        try:
            link = Link.objects.get(id=kwargs['pk'])
            if link.user == bundle.request.user:
                link.delete = True
                link.save()
        except Exception, e:
            print e
        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "links"
        data['response'] = {"links":data["objects"]}
        del(data["objects"])
        return data

    def determine_format(self, request):
        return 'application/json'

class VisitResource(ModelResource):
    class Meta:
        queryset = Visit.objects.all().order_by('-timestamp')
        resource_name = 'visits'
        authorization = DjangoAuthorization()
        authentication = SessionAuthentication()
        limit = 20
        always_return_data = True
        allowed_methods = ['get','post']
        filtering = {}

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(VisitResource, self).build_filters(filters)

        if "document" in filters:
            try:
                month_a_go = datetime.datetime.now() - datetime.timedelta(days=30)
                sqs = Visit.objects.filter(document__id=filters['document'], timestamp__gt=month_a_go).order_by('-timestamp')
                print sqs
            except:
                sqs = []
            if "pk__in" not in orm_filters.keys():
                orm_filters["pk__in"] = []
            orm_filters["pk__in"] = orm_filters["pk__in"] + [i.pk for i in sqs]

        return orm_filters

    def dehydrate(self, bundle):
        """
        Return a list of Visits formatted according to what the developer expects
        """
        return bundle

    def obj_create(self, bundle, **kwargs):
        """
        Creates a new visit
        """
        try:
            document = Document.objects.get(id=bundle.data['document'])
            visit_type = bundle.data['visit_type']
            new_visit = Visit(ip_address=get_client_ip(bundle.request), visit_type=visit_type, document=document)
            if visit_type == 3:
                link = Link.objects.get(id=bundle.data['link'])
                new_visit.link = link
            new_visit.save()
            bundle.obj = new_visit
        except Exception, e:
            print e
        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "visits"
        data['response'] = {"visits":data["objects"]}
        del(data["objects"])
        return data

    def determine_format(self, request):
        return 'application/json'

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class ApplicationResource(ModelResource):
    user = fields.OneToOneField(UserResource, 'user', full=True)
    company = fields.OneToOneField(CompanyResource, 'company', full=True)
    job = fields.OneToOneField(JobResource, 'job', full=True, null=True)
    documents = fields.ToManyField(DocumentResource, 'documents', full=True)
    class Meta:
        queryset = Application.objects.all()
        resource_name = 'applications'
        authorization = DjangoAuthorization()
        authentication = SessionAuthentication()
        limit = 20
        always_return_data = True
        allowed_methods = ['get','post','put','patch']
        filtering = {
            "user": ("exact"), "company": ("exact"), "fair":("exact"), "status":ALL
        }

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(ApplicationResource, self).build_filters(filters)

        # build filters on user, company, fair and status
        sqs = Application.objects.all()
        try:
            if "user_id" in filters:
                user_id = filters['user_id']
                user = User.objects.get(id=user_id)
                sqs = sqs.filter(user=user)
            if "company_id" in filters:
                company_id = filters['company_id']
                company = Company.objects.get(id=company_id)
                sqs = sqs.filter(company=company)
            if "fair_id" in filters:
                fair_id = filters['fair_id']
                fair = Fair.objects.get(id=fair_id)
                sqs = sqs.filter(fair=fair)
            if "unique_students" in filters:
                if filters['unique_students']:
                    sqs = sqs.distinct('user')
        except:
            sqs = []

        if "pk__in" not in orm_filters.keys():
            orm_filters["pk__in"] = []
            orm_filters["pk__in"] = orm_filters["pk__in"] + [i.pk for i in sqs]

        return orm_filters

    def dehydrate(self, bundle):
        """
        Return a list of applications
        """
        if bundle.request.user.is_student:
            del(bundle.data['note'])
        return bundle

    def obj_create(self, bundle, **kwargs):
        """
        two scenarios:
        1. User adds an application as a 'favorite' to keep track himself
        2. User applies through Occhunt for a 357

        Conflict resolution:
        1. If user adds company as favorite initially and then applies through us -> convert application to be managed by us
        2. If user applies to company through us and then tries to favorite it -> don't do anything to original app

        # Scenario 1
        Create a new application
        1. Create a new application with only company and user
        2. Mark added_by_user as True

        This is what gets sent over in json
        'company_id': company_id,
        'added_by_user' True

        # Scenario 2
        Creates a new application
        1. Create a new application
        2. Add application documents to application
        3. Notify user that application is in process

        This is what gets sent over in json
        'company_id': company_id,
        'fair_id': fair_id,
        'resume': selected_resume,
        'cv': selected_cv,
        'docs': selected_docs,
        'position': position,
        'status': 1,
        'majors':majors,
        'grad_year': grad_year,
        'degree_type': degree_type
        """
        try:
            # get all data from POST data
            user = bundle.request.user
            company = Company.objects.get(id=bundle.data['company_id'])
            print company
            if 'added_by_user' in bundle.data.keys() and bundle.data['added_by_user']:
                # check if an application already exists
                application = Application.objects.filter(user=user, company=company)
                if len(application) > 0:
                    application = application[0]
                    bundle.obj = application
                else:
                    application = Application(user=user, company=company, status=6, added_by_user=True)
                    application.save()
                    bundle.obj = application
            else:
                fair = Fair.objects.get(id=bundle.data['fair_id'])
                resume = Document.objects.get(id=bundle.data['resume'])
                if bundle.data['cv']:
                    cv = Document.objects.get(id=bundle.data['cv'])
                else:
                    cv = None
                if bundle.data['docs']:
                    docs = Document.objects.filters(id__in=bundle.data['docs'])
                else:
                    docs = None
                grad_year = bundle.data['grad_year']
                majors = bundle.data['majors']
                degree = Degree.objects.get(id=bundle.data['degree_type'])

                if 'position' in bundle.data.keys():
                    position = bundle.data['position']
                else:
                    position = 'Any'
                if 'status' in bundle.data.keys():
                    status = bundle.data['status']
                else:
                    status = 1

                # 2. Create a new appliation
                # check if an application already exists - either they favorited it or they already applied before
                application = Application.objects.filter(user=user, company=company, fair=fair)
                if len(application) > 0:
                    application = application[0]
                    bundle.obj = application

                    # remove applications where it is not tied to a fair
                    Application.objects.filter(user=user, company=company, fair__isnull=True, added_by_user=True).delete()
                else:
                    now = datetime.datetime.now()
                    application = Application(user=user, company=company, fair=fair, position=position, status=status, student_note='This application will be managed for you till the interview stage. You applied on '+str(now.month)+'/'+str(now.day)+'/'+str(now.year))
                    application.save()
                    bundle.obj = application

                    # remove applications where it is not tied to a fair
                    Application.objects.filter(user=user, company=company, fair__isnull=True, added_by_user=True).delete()

                # 3. Create documents for application
                # resume
                # cv
                # additional docs
                application.documents.add(resume)
                application.save()
                if cv:
                    application.documents.add(cv)
                    application.save()
                if docs:
                    for doc in docs:
                        application.documents.add(document=doc)
                        application.save()

                # update user preferences for Graduation Date, Major, Degree
                try:
                    if grad_year:
                        user.student.graduation_year = grad_year
                        user.student.save()
                except Exception, e:
                    print e
                    # raise e
                try:
                    if majors:
                        for major in majors:
                            major_obj = Major.objects.get(id=int(major))
                            user.student.major.add(major_obj)
                        user.student.save()
                except Exception, e:
                    print e
                    # raise e
                try:
                    if degree:
                        user.student.degree = degree
                        user.student.save()
                except Exception, e:
                    print e
                    # raise e

                # 4. notify user that application has been received
                try:
                    new_notification = Notification(user=user, company=company, receiver=1, notification=1)
                    new_notification.save()
                except Exception, e:
                    print e
                    raise e
            return bundle
        except Exception, e:
            print e
            raise e

    def obj_update(self, bundle, **kwargs):
        """
        Update application status and notes
        """
        try:
            existing_application = Application.objects.get(id=int(kwargs['pk']))
            if 'note' in bundle.data.keys():
                # only recruiters can make notes here
                if bundle.request.user.is_recruiter:
                    existing_application.note = bundle.data['note']
                    existing_application.save()
                    # send notification to student that his app has been viewed
                    try:
                        new_notification = Notification(user=existing_application.user, company=existing_application.company, receiver=1, notification=1)
                        new_notification.save()
                    except Exception, e:
                        print e
                        raise e
            if 'student_note' in bundle.data.keys():
                # when the student makes a note
                existing_application.student_note = bundle.data['student_note']
                existing_application.save()
            if 'status' in bundle.data.keys():
                existing_application.status = bundle.data['status']
                if 'recruiter_email' in bundle.data.keys():
                    # update recruiter_email - email address
                    existing_application.recruiter_email = bundle.data['recruiter_email']
                if 'recruiter_message' in bundle.data.keys():
                    # update recruiter_message
                    existing_application.recruiter_message = bundle.data['recruiter_message']

                existing_application.save()
                
            bundle.obj = existing_application
        except Exception, e:
            print e
            raise e
        return bundle

    def authorized_read_list(self, object_list, bundle):
        if bundle.request.user.is_student:
            return object_list.filter(user=bundle.request.user)
        if bundle.request.user.is_recruiter:
            return object_list.filter(company__id=bundle.request.user.recruiter.company.id)

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "applications"
        data['response'] = {"applications":data["objects"]}
        del(data["objects"])
        return data

    def determine_format(self, request):
        return 'application/json'

class ApplicationSearchResource(ModelResource):
    user = fields.OneToOneField(UserResource, 'user', full=True)
    company = fields.OneToOneField(CompanyResource, 'company', full=True)
    job = fields.OneToOneField(JobResource, 'job', full=True, null=True)
    documents = fields.ToManyField(DocumentResource, 'documents', full=True)
    class Meta:
        queryset = Application.objects.all()
        resource_name = 'applicationsearch'
        authorization = DjangoAuthorization()
        authentication = RecruiterAuthentication()
        limit = 0
        always_return_data = True
        allowed_methods = ['get']

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(ApplicationSearchResource, self).build_filters(filters)

        # 1. tokenize skills
        # 2. create OR query for each token
        # The queries are ORed within a category and AND between categories
        q_objects = Q()
        # if "skills" in filters:
        #     tokens = filters['skills'].split(',')
        #     skills_q = Q(documents__description__contains=str(tokens[0]))
        #     for token in tokens:
        #         skills_q |= Q(documents__description__contains=str(token))
        #     q_objects &= skills_q
        if "schools" in filters:
            tokens = filters['schools'].split(',')
            schools_q = Q(user__groups__id=tokens[0])
            for token in tokens:
                schools_q |= Q(user__groups__id=token)
            q_objects &= schools_q
        if "categories" in filters:
            tokens = filters['categories'].split(',')
            categories_q = Q(status=tokens[0])
            for token in tokens:
                categories_q |= Q(status=token)
            q_objects &= categories_q
        # if "offers" in filters:
        #     tokens = filters['offers'].split(',')
        #     for token in tokens:
        #         sqs.filter()
        if "positions" in filters:
            tokens = filters['positions'].split(',')
            positions_q = Q(position=str(tokens[0]))
            for token in tokens:
                positions_q |= Q(position=str(token))
            q_objects &= positions_q
        if "majors" in filters:
            tokens = filters['majors'].split(',')
            for token in tokens:
                sqs.filter(user__student__major__id=token)
        if "degrees" in filters:
            tokens = filters['degrees'].split(',')
            degrees_q = Q(user__student__degree__id=token[0])
            for token in tokens:
                degrees_q |= Q(user__student__degree__id=token)
            q_objects &= degrees_q
        if "gradyears" in filters:
            tokens = filters['gradyears'].split(',')
            gradyears_q = Q(user__student__graduation_year=int(tokens[0]))
            for token in tokens:
                gradyears_q |= Q(user__student__graduation_year=int(token))
            q_objects &= gradyears_q
        if "notes" in filters:
            tokens = filters['notes'].split(',')
            if '1' in tokens and '0' not in tokens:
                q_objects &= Q(note__gt='')
            if '1' not in tokens and '0' in tokens:
                q_objects &= Q(note__exact='')

        print q_objects
        # only show Application that are new (i.e. from the last 357s and those with offers that are not expired)
        sqs = Application.objects.filter(q_objects)

        if "pk__in" not in orm_filters.keys():
            orm_filters["pk__in"] = []
        orm_filters["pk__in"] = orm_filters["pk__in"] + [i.pk for i in sqs]

        return orm_filters

    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(company__id=bundle.request.user.recruiter.company.id)

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "applications"
        data['response'] = {"applications":data["objects"]}
        del(data["objects"])
        return data

    def determine_format(self, request):
        return 'application/json'
