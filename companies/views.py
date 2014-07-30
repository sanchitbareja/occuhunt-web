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
from haystack.query import SearchQuerySet

from companies.models import Company
from applications.models import Application
from jobs.models import Job

def home(request):
    """Home view"""
    return render_to_response('index.html', {"fairs_link":True},
                                  RequestContext(request))

def splash(request):
    """Splash view"""
    return render_to_response('homepage2.html', {},
                                  RequestContext(request))

def companies(request):
    """Companies view"""
    return render_to_response('companies.html', {"companies_link":True},
                                  RequestContext(request))


def search(request):
    """Search companies view"""
    return render_to_response('search.html', {"search_link":True},
                                  RequestContext(request))

def search_query(request):
    """Search companies view"""
    query = request.GET['q']
    search_results = SearchQuerySet().models(Company).load_all().auto_query(query)
    print search_results
    data_to_send = {
      'companies':search_results
    }
    return render_to_response('search_results.html', data_to_send, RequestContext(request))

def company(request, companyID):
    """Individual Company view"""
    try:
        company = Company.objects.get(id=companyID)
        public_jobs = Job.objects.filter(network__isnull=True,company=company)
        if not request.user.is_authenticated():
            return render_to_response('company.html', {'company': company, 'jobs':public_jobs},
                                  RequestContext(request))
        else:
            favorite = Application.objects.filter(company=company, user__id=request.user.id)
            filtered_jobs = []
            is_favorited = False
            if len(favorite) > 0:
                is_favorited = True
            if len(request.user.groups.filter(name="UC Berkeley")) > 0:
                filtered_jobs = Job.objects.filter(network__name="UC Berkeley").filter(company=company)
            all_jobs = list(chain(filtered_jobs, public_jobs))
            return render_to_response('company.html', {'company': company, 'is_favorited':is_favorited, 'jobs':all_jobs},
                                  RequestContext(request))
    except Exception as e:
      print e
      raise Http404('Sorry, no company found :(');
