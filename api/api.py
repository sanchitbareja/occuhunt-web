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
from fairs.models import Fair, Room
from users.models import User, Major, Degree, Student, Recruiter
from resumes.models import Resume, Comment
from recommendations.models import Recommendation, Request
from hunts.models import Hunt
from applications.models import Application
from jobs.models import Job
from notifications.models import Notification
import datetime,json



class CompanyResource(ModelResource):
    class Meta:
        queryset = Company.objects.all()
        resource_name = 'companies'
        # Add it here.
        # authentication = BasicAuthentication()
        limit = 0
        authorization = DjangoAuthorization()

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
        Return a list of clubs formatted according to what the developer expects
        """
        favorite_objects = Favorite.objects.filter(company=bundle.obj.id)
        favorites = [fav.user.id for fav in favorite_objects]
        bundle.data['favorites'] = favorites
        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "response"
        data['response'] = {"companies":data['objects']}
        del(data['objects'])
        return data

    def determine_format(self, request):
        return 'application/json'

class StudentResource(ModelResource):
    class Meta:
        queryset = Student.objects.all()
        resource_name = 'users'
        # Add it here.
        # authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

        allowed_methods = ['get']
        filtering = {
            "first_name": ("exact"), "linkedin_uid": ("exact"),
        }
        excludes = ['password','last_login','is_active','is_admin','time_created']

    def dehydrate(self, bundle):
        """
        Return a list of clubs formatted according to what the developer expects
        """
        # get resume
        resume = Resume.objects.filter(user__id=bundle.data['id'], showcase=True, original=False).order_by('-timestamp')
        if len(resume) > 0:
            resume = resume[0]
            bundle.data['resume'] = resume.url
        else:
            resume = None
            bundle.data['resume'] = None

        # get school
        bundle.data['school'] = [name for name in bundle.obj.groups.values('name')]

        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "response"
        data['response'] = {"users":data['objects']}
        del(data['objects'])
        return data

    def determine_format(self, request):
        return 'application/json'

class UserResource(ModelResource):
    recruiter_for = fields.OneToOneField(CompanyResource, 'recruiter.company', full=True, null=True)
    graduation_year = fields.IntegerField(attribute='student.graduation_year', null=True)
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        # Add it here.
        # authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

        allowed_methods = ['get']
        filtering = {
            "first_name": ("exact"), "linkedin_uid": ("exact"),
        }
        excludes = ['password','last_login','is_active','is_admin','time_created']

    def dehydrate(self, bundle):
        """
        Return a list of clubs formatted according to what the developer expects
        """
        # get resume
        resume = Resume.objects.filter(user__id=bundle.data['id'], showcase=True, original=False).order_by('-timestamp')
        if len(resume) > 0:
            resume = resume[0]
            bundle.data['resume'] = resume.url
        else:
            resume = None
            bundle.data['resume'] = None

        # get school
        bundle.data['school'] = [name for name in bundle.obj.groups.values('name')]

        # get graduation_year, major, degree
        # check if student
        if bundle.obj.is_student:
            bundle.data['graduation_year'] = bundle.obj.student.graduation_year
            bundle.data['degree'] = bundle.obj.student.degree
            bundle.data['majors'] = [major["major"] for major in bundle.obj.student.major.values('major')]
            
        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "response"
        data['response'] = {"users":data['objects']}
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
        # authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
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
            print "1"
            if bundle.data['unfavorite']:
                print "2"
                a = Favorite.objects.filter(user=user).filter(company=company)
                a.delete()
            else:
                print "3"
                old_favorite = Favorite.objects.filter(user=user, company=company)
                if len(old_favorite) > 0:
                    print "4"
                    bundle.obj = old_favorite[0]
                else:
                    print "5"
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

class RoomResource(ModelResource):
    class Meta:
        queryset = Room.objects.all()
        resource_name = 'rooms'
        # Add it here.
        # authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

        allowed_methods = ['get']

    def determine_format(self, request):
        return 'application/json'

class FairResource(ModelResource):
    rooms = fields.ManyToManyField(RoomResource, 'rooms', full=True)
    class Meta:
        queryset = Fair.objects.all().order_by('-time_start')
        resource_name = 'fairs'
        # Add it here.
        # authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

        allowed_methods = ['get']

    def determine_format(self, request):
        return 'application/json'

class CommentResource(ModelResource):
    user = fields.OneToOneField(UserResource, 'user', full=True)
    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'comments'
        # Add it here.
        # authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
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
        # Add it here.
        # authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        limit = 20
        always_return_data = True
        allowed_methods = ['get','post']
        filtering = {
            "featured": ("exact"), "user": ("exact"), "showcase": ("exact")
        }

    def dehydrate(self, bundle):
        """
        Return a list of resumes formatted according to what the developer expects
        """

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

class RecommendationRequestResource(ModelResource):
    class Meta:
        queryset = Request.objects.all()
        resource_name = 'recommendation_requests'
        authorization = DjangoAuthorization()
        limit = 100
        always_return_data = False
        allowed_methods = ['get', 'post']
        filtering = {
            "request_from": ("exact"),
            "request_to": ("exact")
        }
        excludes = ['relationship','project']

    def dehydrate(self, bundle):
        """
        Return a list of recommendation requests
        """

        return bundle

    def obj_create(self, bundle, **kwargs):
        """
        Creates a new recommendation request
        """
        try:
            new_request = Request(request_from=bundle.data['from'],request_to=bundle.data['to'],relationship=bundle.data['relationship'],project=bundle.data['project'],message=bundle.data['message'])
            new_request.save()
            bundle.obj = new_request
        except Exception, e:
            print e
        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "requests"
        data['response'] = {"requests":data["objects"]}
        del(data["objects"])
        return data

    def determina_format(self, request):
        return 'application/json'

class RecommendationResource(ModelResource):
    class Meta:
        queryset = Recommendation.objects.all()
        resource_name = 'recommendations'
        authorization = DjangoAuthorization()
        limit = 100
        always_return_data = False
        allowed_methods = ['get','post']
        filtering = {
            "recommendation_from": ("exact"),
            "recommendation_to": ("exact")
        }

    def dehydrate(self, bundle):
        """
        Return a list of recommendations
        """

        return bundle

    def obj_create(self, bundle, **kwargs):
        """
        Creates a new recommendation
        """
        try:
            if bundle.data['replied'] != None:
                try:
                    request_obj = Request.objects.get(id=bundle.data['replied'])
                    request_obj.replied = True
                    request_obj.save()
                except Exception, e:
                    print e
            new_rec = Recommendation(recommendation_from=bundle.data["from"], recommendation_to=bundle.data["to"],relationship=bundle.data["relationship"],project=bundle.data["project"],answer1=bundle.data["answer1"],answer2=bundle.data["answer2"],answer3=bundle.data["answer3"])
            new_rec.save()
            bundle.obj = new_rec
        except Exception, e:
            print e
        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "recommendations"
        data["response"] = {"recommendations":data["objects"]}
        del(data["objects"])
        return data

    def determine_format(self, request):
        return 'application/json'

class HuntResource(ModelResource):
    user = fields.OneToOneField(UserResource, 'user', full=True)
    fair = fields.OneToOneField(FairResource, 'fair', full=True)
    class Meta:
        queryset = Hunt.objects.all()
        resource_name = 'hunts'
        authorization = DjangoAuthorization()
        limit = 100
        always_return_data = True
        allowed_methods = ['get','post']
        filtering = {
            "user": ("exact"), "fair": ("exact")
        }

    def dehydrate(self, bundle):
        """
        Return a list of hunts
        """
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

class ApplicationResource(ModelResource):
    user = fields.OneToOneField(UserResource, 'user', full=True)
    fair = fields.OneToOneField(FairResource, 'fair', full=True)
    company = fields.OneToOneField(CompanyResource, 'company', full=True)
    class Meta:
        queryset = Application.objects.all()
        resource_name = 'applications'
        authorization = DjangoAuthorization()
        limit = 10000
        always_return_data = 100
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
            if "grad_year" in filters:
                grad_year = filters['grad_year']
                sqs = sqs.filter(user__student__graduation_year=grad_year)
            if "degree_type" in filters:
                degree_type = filters['degree_type']
                sqs = sqs.filter(user__student__degree__id=degree_type)
            if "major" in filters:
                degree_type = filters['major']
                sqs = sqs.filter(user__student__major__id=degree_type)
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
        return bundle

    def obj_create(self, bundle, **kwargs):
        """
        Creates a new application
        """
        try:
            user = User.objects.get(id=bundle.data['user_id'])
            print user
            company = Company.objects.get(id=bundle.data['company_id'])
            print company
            fair = Fair.objects.get(id=bundle.data['fair_id'])
            print fair
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

            # update user preferences for Graduation Date, Major, Degree
            try:
                grad_year = bundle.data['grad_year']
                user.student.graduation_year = grad_year
                user.student.save()
            except Exception, e:
                print e
                # raise e
            try:
                majors = bundle.data['majors']
                for major in majors:
                    major_obj = Major.objects.get(id=int(major))
                    user.student.major.add(major_obj)
                user.student.save()
            except Exception, e:
                print e
                # raise e
            try:
                degree = Degree.objects.get(id=bundle.data['degree_type'])
                user.student.degree = degree
                user.student.save()
            except Exception, e:
                print e
                # raise e

            # notify user that application has been viewed by company
            try:
                # bug here as this is only true if the company added is on the iPad
                # works out well for the user though as he feels wanted
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

class JobResource(ModelResource):
    company = fields.OneToOneField(CompanyResource, 'company', full=True)
    class Meta:
        queryset = Job.objects.all()
        resource_name = 'jobs'
        authorization = DjangoAuthorization()
        limit = 100
        always_return_data = True
        allowed_methods = ['get','post', 'put']
        filtering = {}

    def obj_create(self, bundle, **kwargs):
        """
        Create or delete a new job
        """
        print 1
        try:
            if 'deactivate' in bundle.data.keys() and bundle.data['deactivate']:
                print 2
                existing_job = Job.objects.get(id=bundle.data['job_id'])
                existing_job.deactivate = True
                existing_job.save()
                bundle.obj = existing_job
            else:
                print 3
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

    def determine_format(self, request):
        return 'application/json'