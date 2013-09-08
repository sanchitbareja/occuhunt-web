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
import datetime


class CompanyResource(ModelResource):
    class Meta:
        queryset = Company.objects.all()
        resource_name = 'companies'
        # Add it here.
        # authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

        allowed_methods = ['get']
        filtering = {
            "name": ("exact")
        }

    def dehydrate(self, bundle):
        """
        Return a list of clubs formatted according to what the developer expects
        """
        # # no renaming required for 'name'
        # bundle.data['name'] = bundle.obj.name

        # # no renaming required for 'description'
        # bundle.data['description'] = bundle.obj.description

        # # no renaming required for 'typeOfOrganization'
        # bundle.data['typeOfOrganization'] = bundle.obj.typeOfOrganization

        # # no renaming required for 'urlPersonal'
        # bundle.data['urlPersonal'] = bundle.obj.urlPersonal

        # # rename 'image' to 'imageUrl'
        # bundle.data['imageUrl'] = bundle.obj.image
        # del(bundle.data['image'])

        # # no renaming required for 'founded'
        # bundle.data['founded'] = bundle.obj.founded

        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "response"
        # data['response'] = {"clubs":data['objects']}
        # del(data['objects'])
        return data

    def determine_format(self, request):
        return 'application/json'