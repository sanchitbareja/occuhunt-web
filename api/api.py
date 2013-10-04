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

# misc
from django.db.models import Q
from companies.models import Company
from favorites.models import Favorite
from fairs.models import Fair
from users.models import User
from hunting.models import Hunting
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
            "first_name": ("exact")
        }
        excludes = ['password','last_login','is_active','is_admin','is_superuser']

    def dehydrate(self, bundle):
        """
        Return a list of clubs formatted according to what the developer expects
        """

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
            "name": ("exact")
        }

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

class FairResource(ModelResource):
    class Meta:
        queryset = Fair.objects.all()
        resource_name = 'fairs'
        # Add it here.
        # authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

        allowed_methods = ['get']

    def determine_format(self, request):
        return 'application/json'

class HuntingResource(ModelResource):
    fair = fields.OneToOneField(FairResource, 'fair', full=True)
    user = fields.OneToOneField(UserResource, 'user', full=True)
    class Meta:
        queryset = Hunting.objects.all()
        resource_name = 'hunting'
        # Add it here.
        # authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        limit = 0
        allowed_methods = ['get','post']

    def dehydrate(self, bundle):
        """
        Return a list of clubs formatted according to what the developer expects
        """

        return bundle

    def obj_create(self, bundle, **kwargs):
        """
        Posts a new "hunt"
        """
        user = User.objects.get(id=bundle.data["user"])
        fair = Fair.objects.get(id=bundle.data["fair"])
        old_hunting = Hunting.objects.filter(user=user).filter(fair=fair)
        if len(old_hunting) <= 0:
            new_hunting = Hunting(user=user, fair=fair)
            new_hunting.save()
            bundle.obj = new_hunting
        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "response"
        data['response'] = {"favorites":data['objects']}
        del(data['objects'])
        return data

    def determine_format(self, request):
        return 'application/json'