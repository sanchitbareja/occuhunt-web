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
from users.models import User
from resumes.models import Resume, Comment
from recommendations.models import Recommendation, Request
from hunts.models import Hunt
from applications.models import Application, Note
import datetime


class UserResource(ModelResource):
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

        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "response"
        data['response'] = {"users":data['objects']}
        del(data['objects'])
        return data

    def determine_format(self, request):
        return 'application/json'

class CompanyResource(ModelResource):
    class Meta:
        queryset = Company.objects.all()
        resource_name = 'companies'
        # Add it here.
        # authentication = BasicAuthentication()
        limit = 0
        authorization = DjangoAuthorization()

        allowed_methods = ['get']
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
        user = User.objects.get(id=bundle.data["user"])
        company = Company.objects.get(id=bundle.data["company"])
        if bundle.data['unfavorite']:
            a = Favorite.objects.filter(user=user).filter(company=company)
            a.delete()
        else:
            new_favorite = Favorite(user=user, company=company)
            new_favorite.save()
            bundle.obj = new_favorite
        return bundle

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
        queryset = Fair.objects.all().order_by('-date_start')
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

class RecruiterNotesResource(ModelResource):
    user = fields.OneToOneField(UserResource, 'user', full=True)
    recruiter = fields.OneToOneField(UserResource, 'recruiter', full=True)
    class Meta:
        queryset = Note.objects.all()
        resource_name = 'notes'
        authorization = DjangoAuthorization()
        limit = 100
        always_return_data = True
        allowed_methods = ['get','post']
        filtering = {
            "user": ("exact"), "recruiter": ("exact")
        }

    def dehydrate(self, bundle):
        """
        Return a list of resumedrops
        """
        return bundle

    def obj_create(self, bundle, **kwargs):
        """
        Creates a new resumedrop
        """
        try:
            user = User.objects.get(id=bundle.data['user_id'])
            recruiter = User.objects.get(id=bundle.data['recruiter_id'])
            new_note = Note(user=user, recruiter=recruiter, note=bundle.data['note'])
            new_note.save()
            bundle.obj = new_note
        except Exception, e:
            raise e
        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "resumedrops"
        data['response'] = {"notes":data["objects"]}
        del(data["objects"])
        return data

    def determine_format(self, request):
        return 'application/json'
