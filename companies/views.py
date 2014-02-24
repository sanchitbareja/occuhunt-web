from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django import forms
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import os, time, simplejson
from datetime import datetime, timedelta, time
from django.http import Http404
from itertools import chain

from social_auth import __version__ as version
from social_auth.utils import setting

from companies.models import Company
from favorites.models import Favorite
from jobs.models import Job

def home(request):
    """Home view"""
    return render_to_response('index.html', {'version': version, "fairs_link":True},
                                  RequestContext(request))

def splash(request):
    """Splash view"""
    return render_to_response('splash.html', {'version': version},
                                  RequestContext(request))


def companies(request):
    """Companies view"""
    return render_to_response('companies.html', {'version': version, "companies_link":True},
                                  RequestContext(request))


def search(request):
    """Search companies view"""
    return render_to_response('search.html', {'version': version, "search_link":True},
                                  RequestContext(request))


def company(request, companyID):
    """Individual Company view"""
    try:
        company = Company.objects.get(id=companyID)
        public_jobs = Job.objects.filter(network__isnull=True,company=company)
        if not request.user.is_authenticated():
            return render_to_response('company.html', {'version': version, 'company': company, 'job':public_jobs},
                                  RequestContext(request))
        else:
            favorite = Favorite.objects.filter(company=company, user__id=request.user.id)
            filtered_jobs = None
            is_favorited = False
            if len(favorite) > 0:
                is_favorited = True
            if len(request.user.groups.filter(name="UC Berkeley")) > 0:
              filtered_jobs = Job.objects.filter(network__name="UC Berkeley").filter(company=company)
              all_jobs = list(chain(filtered_jobs, public_jobs))
            return render_to_response('company.html', {'version': version, 'company': company, 'is_favorited':is_favorited, 'jobs':all_jobs},
                                  RequestContext(request))
    except Exception as e:
      print e
      raise Http404('Sorry, no company found :(');
