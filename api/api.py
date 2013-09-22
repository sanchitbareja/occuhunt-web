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

        allowed_methods = ['get','post']
        filtering = {
            "user": ("exact")
        }

    def dehydrate(self, bundle):
        """
        Return a list of clubs formatted according to what the developer expects
        """

        return bundle

    def obj_create(self, bundle, **kwargs):
        """
        Posts a new favorite
        """
        print "11"
        print bundle.data
        print '12'
        print bundle.data['user']
        print bundle.data['company']
        print bundle.data["unfavorite"]
        user = User.objects.get(id=bundle.data["user"])
        company = Company.objects.get(id=bundle.data["company"])
        print user
        print company.id
        print "22"
        if bundle.data['unfavorite']:
            print "23"
            a = Favorite.objects.filter(user=user).filter(company=company)
            print a
            a.delete()
            # bundle.obj = None
        else:
            print "24"
            new_favorite = Favorite(user=user, company=company)
            new_favorite.save()
            bundle.obj = new_favorite
        print "33"
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
        filtering = {
            "user": ("exact")
        }

    def dehydrate(self, bundle):
        """
        Return a list of clubs formatted according to what the developer expects
        """

        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "response"
        data['response'] = {"favorites":data['objects']}
        del(data['objects'])
        return data

    def determine_format(self, request):
        return 'application/json'