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
from authentication import OAuth20Authentication

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
from users.models import User, Student, Recruiter
from resumes.models import Resume, Comment
from recommendations.models import Recommendation, Request
from hunts.models import Hunt
from applications.models import Application
from jobs.models import Job
from notifications.models import Notification
from documents.models import Document, Link, Visit
import datetime, json, random, string

class CompanyResource(ModelResource):
    class Meta:
        queryset = Company.objects.all()
        resource_name = 'companies'
        limit = 20
        authorization = DjangoAuthorization()
        authentication = OAuth20Authentication()

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
        authentication = OAuth20Authentication()

        allowed_methods = ['get']
        filtering = {
            "first_name": ("exact"), "linkedin_uid": ("exact"),
        }
        excludes = ['password','last_login','is_active','is_admin','time_created']

    def dehydrate(self, bundle):
        """
        Return a list of users formatted according to what the developer expects
        """
        # get resume - only recruiter should be able to see resume
        if bundle.request.user.is_recruiter:
            resume = Resume.objects.filter(user__id=bundle.data['id'], showcase=True, original=False).order_by('-timestamp')
            if len(resume) > 0:
                resume = resume[0]
                bundle.data['resume'] = resume.url
            else:
                resume = None
                bundle.data['resume'] = None

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
        authentication = OAuth20Authentication()

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

class FavoriteResource(ModelResource):
    user = fields.OneToOneField(UserResource, 'user', full=True)
    company = fields.OneToOneField(CompanyResource, 'company', full=True)
    class Meta:
        queryset = Favorite.objects.all()
        resource_name = 'favorites'
        # Add it here.
        authorization = DjangoAuthorization()
        authentication = OAuth20Authentication()
        always_return_data = False
        allowed_methods = ['get','post','put']
        filtering = {
            "user": ("exact")
        }

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(FavoriteResource, self).build_filters(filters)

        if "user_id" in filters:
            try:
                user_id = filters['user_id']
                user = User.objects.get(id=user_id)
                sqs = Favorite.objects.filter(user=user)
            except:
                sqs = []
            if "pk__in" not in orm_filters.keys():
                orm_filters["pk__in"] = []
            orm_filters["pk__in"] = orm_filters["pk__in"] + [i.pk for i in sqs]

        return orm_filters

    def dehydrate(self, bundle):
        """
        Return a list of clubs formatted according to what the developer expects
        """

        return bundle

    def obj_create(self, bundle, **kwargs):
        """
        Posts a new favorite
        """
        try:
            try:
                user = User.objects.get(id=bundle.data["user_id"])
                company = Company.objects.get(id=bundle.data["company_id"])
            except:
                user = User.objects.get(id=bundle.data["user"])
                company = Company.objects.get(id=bundle.data["company"])
            if bundle.data['unfavorite']:
                a = Favorite.objects.filter(user=user).filter(company=company)
                a.delete()
            else:
                old_favorite = Favorite.objects.filter(user=user, company=company)
                if len(old_favorite) > 0:
                    bundle.obj = old_favorite[0]
                else:
                    new_favorite = Favorite(user=user, company=company)
                    new_favorite.save()
                    bundle.obj = new_favorite
            return bundle
        except Exception, e:
            print e

    def obj_update(self, bundle, **kwargs):
        """
        Updates an existing favorite
        """
        favorite = Favorite.objects.get(id=bundle.data["favorite"])
        if bundle.data['note']:
            favorite.note = bundle.data['note']
        if bundle.data['category']:
            favorite.category = bundle.data['category']
        favorite.save()
        bundle.obj = favorite
        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "response"
        data['response'] = {"favorites":data['objects']}
        del(data['objects'])
        return data

    def determine_format(self, request):
        return 'application/json'

class HuntResource(ModelResource):
    user = fields.OneToOneField(UserResource, 'user', full=True)
    fair = fields.OneToOneField(FairResource, 'fair')
    class Meta:
        queryset = Hunt.objects.all()
        resource_name = 'hunts'
        authorization = DjangoAuthorization()
        authentication = OAuth20Authentication()
        limit = 20
        always_return_data = True
        allowed_methods = ['get','post']
        filtering = {
            "user": ("exact"), "fair": ("exact")
        }

    def dehydrate(self, bundle):
        """
        Return a list of hunts
        """
        bundle.data['fair'] = bundle.obj.fair.id
        return bundle

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(HuntResource, self).build_filters(filters)

        if "user_id" in filters:
            sqs = Hunt.objects.filter(user__id=filters['user_id'])

            orm_filters["pk__in"] = [i.pk for i in sqs]

        # build filters on user, company, fair and status
        sqs = Hunt.objects.all()
        try:
            if "user_id" in filters:
                user_id = filters['user_id']
                user = User.objects.get(id=user_id)
                sqs = sqs.filter(user=user)
            if "fair_id" in filters:
                fair_id = filters['fair_id']
                fair = Fair.objects.get(id=fair_id)
                sqs = sqs.filter(fair=fair)
        except:
            sqs = []

        if "pk__in" not in orm_filters.keys():
            orm_filters["pk__in"] = []
            orm_filters["pk__in"] = orm_filters["pk__in"] + [i.pk for i in sqs]

        return orm_filters

    def obj_create(self, bundle, **kwargs):
        """
        Creates a new hunt
        """
        try:
            user = User.objects.get(id=bundle.data['user_id'])
            fair = Fair.objects.get(id=bundle.data['event_id'])
            old_hunt = Hunt.objects.filter(user=user, fair=fair)
            if len(old_hunt) > 0:
                bundle.obj = old_hunt[0]
            else:
                new_hunt = Hunt(user=user, fair=fair)
                new_hunt.save()
                bundle.obj = new_hunt
        except Exception, e:
            raise e
        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "hunts"
        data['response'] = {"hunts":data["objects"]}
        del(data["objects"])
        return data

    def determine_format(self, request):
        return 'application/json'

class JobResource(ModelResource):
    company = fields.OneToOneField(CompanyResource, 'company', full=True)
    class Meta:
        queryset = Job.objects.all()
        resource_name = 'jobs'
        authorization = DjangoAuthorization()
        authentication = OAuth20Authentication()
        limit = 20
        always_return_data = True
        allowed_methods = ['get','post', 'put']
        filtering = {}

    def dehydrate(self, bundle):
        """
        Return a list of jobs in format as expected by developer
        """
        # get network
        bundle.data['network'] = {'name':bundle.obj.network.name, 'id':bundle.obj.network.id}
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
        authentication = OAuth20Authentication()
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

class CommentResource(ModelResource):
    user = fields.OneToOneField(UserResource, 'user', full=True)
    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'comments'
        # Add it here.
        authorization = DjangoAuthorization()
        authentication = OAuth20Authentication()
        limit = 0
        always_return_data = True
        allowed_methods = ['post']

    def dehydrate(self, bundle):
        """
        Return a list of comments for a given resume
        """
        return bundle

    def obj_create(self, bundle, **kwargs):
        """
        Creates a new comment
        """
        user = User.objects.get(id=bundle.data["user"])
        user.resume_points += 2
        user.save()
        resume = Resume.objects.get(id=bundle.data['resume'])
        new_comment = Comment(user=user, resume=resume, x=bundle.data['x'], y=bundle.data['y'], comment=bundle.data['comment'])
        new_comment.save()
        bundle.obj = new_comment
        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "comments"
        data['response'] = {"comments":data["objects"]}
        del(data["objects"])
        return data

    def determine_format(self, request):
        return 'application/json'

class ResumeResource(ModelResource):
    user = fields.OneToOneField(UserResource, 'user', full=True)
    comments = fields.ManyToManyField('api.api.CommentResource', 'comment_set', full=True)
    class Meta:
        queryset = Resume.objects.filter(original=False).order_by('-timestamp')
        resource_name = 'resumes'
        authorization = DjangoAuthorization()
        authentication = OAuth20Authentication()
        limit = 20
        always_return_data = True
        allowed_methods = ['get','post']
        filtering = {
            "featured": ("exact"), "user": ("exact"), "showcase": ("exact"), "anonymous": ("exact")
        }

    def dehydrate(self, bundle):
        """
        Return a list of resumes formatted according to what the developer expects
        """
        # user will be anonymous if obj.anonymous = True
        if bundle.obj.anonymous:
            bundle.data['user'] = "anonymous"

        return bundle

    def obj_create(self, bundle, **kwargs):
        """
        Creates a new resume
        """
        try:
            user = User.objects.get(id=bundle.data["user"])
            if bundle.data['featured']:
                user.resume_points -= 20
                user.save()
            # need to check if url, anonymous, original supplied
            new_resume = Resume(user=user, url=bundle.data['url'], anonymous=bundle.data['anonymous'], original=bundle.data['original'], featured=bundle.data['featured'], showcase=bundle.data['showcase'])
            new_resume.save()
            bundle.obj = new_resume
        except Exception, e:
            print e
        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "resumes"
        data['response'] = {"resumes":data["objects"]}
        del(data["objects"])
        return data

    def determine_format(self, request):
        return 'application/json'

class ApplicationResource(ModelResource):
    user = fields.OneToOneField(UserResource, 'user', full=True)
    company = fields.OneToOneField(CompanyResource, 'company', full=True)
    job = fields.OneToOneField(JobResource, 'job', full=True, null=True)
    class Meta:
        queryset = Application.objects.all()
        resource_name = 'applications'
        authorization = DjangoAuthorization()
        authentication = OAuth20Authentication()
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
        bundle.data['fair'] = bundle.obj.fair.id
        if bundle.request.user.is_student:
            del(bundle.data['status'])
            del(bundle.data['note'])
        return bundle

    def obj_create(self, bundle, **kwargs):
        """
        Creates a new application
        """
        try:
            user = User.objects.get(id=bundle.data['user_id'])
            company = Company.objects.get(id=bundle.data['company_id'])
            fair = Fair.objects.get(id=bundle.data['fair_id'])
            if 'position' in bundle.data.keys():
                position = bundle.data['position']
            else:
                position = 'Any'
            if 'status' in bundle.data.keys():
                status = bundle.data['status']
            else:
                status = 1
            # auto-checkin the user
            old_checkin = Hunt.objects.filter(user=user, fair=fair)
            if not len(old_checkin) > 0:
                new_checkin = Hunt(user=user, fair=fair)
                new_checkin.save()
            # check if an application already exists
            old_application = Application.objects.filter(user=user, company=company, fair=fair)
            if len(old_application) > 0:
                bundle.obj = old_application[0]
            else:
                new_application = Application(user=user, company=company, fair=fair, status=status, position=position)
                new_application.save()
                bundle.obj = new_application
            # notify user that application has been viewed by company
            try:
                new_notification = Notification(user=user, company=company, receiver=1, notification=1)
                new_notification.save()
            except Exception, e:
                print e
                raise e
        except Exception, e:
            print e
            raise e
        return bundle

    def obj_update(self, bundle, **kwargs):
        """
        Update application status and notes
        """
        try:
            existing_application = Application.objects.get(id=int(kwargs['pk']))
            if 'note' in bundle.data.keys():
                existing_application.note = bundle.data['note']
                existing_application.save()
                # send notification to student that his app has been viewed
                try:
                    new_notification = Notification(user=existing_application.user, company=existing_application.company, receiver=1, notification=1)
                    new_notification.save()
                except Exception, e:
                    print e
                    raise e
            if 'status' in bundle.data.keys():
                existing_application.status = bundle.data['status']
                existing_application.save()
                # send notification to student that his status has been updated
                try:
                    if bundle.data['status'] == 1 or bundle.data['status'] == 2:
                        new_notification = Notification(user=existing_application.user, company=existing_application.company, receiver=1, notification=1)
                        new_notification.save()
                    if bundle.data['status'] == 3:
                        new_notification = Notification(user=existing_application.user, company=existing_application.company, receiver=1, notification=3)
                        new_notification.save()
                    if bundle.data['status'] == 4:
                        new_notification = Notification(user=existing_application.user, company=existing_application.company, receiver=1, notification=4)
                        new_notification.save()
                except Exception, e:
                    print e
                    raise e
            bundle.obj = existing_application
        except Exception, e:
            print e
            raise e
        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "applications"
        data['response'] = {"applications":data["objects"]}
        del(data["objects"])
        return data

    def determine_format(self, request):
        return 'application/json'


class DocumentResource(ModelResource):
    user = fields.OneToOneField(UserResource, 'user', full=True)
    class Meta:
        queryset = Document.objects.all().order_by('-timestamp')
        resource_name = 'documents'
        authorization = DjangoAuthorization()
        authentication = OAuth20Authentication()
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
        authentication = OAuth20Authentication()
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
        authentication = OAuth20Authentication()
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
