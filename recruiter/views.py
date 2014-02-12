from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django import forms
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import os, time, simplejson, base64, urllib, hmac, sha, random, string
from string import strip
from django.http import Http404
from django.core import serializers

from occuhunt.settings import EMAIL_MASTERS
from companies.models import Company
from jobs.models import Job

from social_auth import __version__ as version
from social_auth.utils import setting

def recruiter_hire(request):
    """Recruiter interface for hiring candidates"""
    return render_to_response('recruiter/recruiter_hire.html', {'version': version}, RequestContext(request))

def recruiter_market(request):
    """Recruiter interface for editting their profile"""
    company = Company.objects.get(id=302)
    jobs = Job.objects.filter(company=company)
    return render_to_response('recruiter/recruiter_market.html', {'version': version, 'company':company}, RequestContext(request))

def recruiter_sell(request):
    """Recruiter interface for sponsoring events"""
    return render_to_response('recruiter/recruiter_sell.html', {'version': version}, RequestContext(request))

def recruiter_sponsorship_request(request):
    """post sponsorship request form and send email"""
    results = {'success':False}
    if(request.method == u'POST'):
        POST = request.POST
        send_mail('[Occuhunt] Recruiter Sponsorship Request!', POST['sponsorRequest']+" Recruiter ID: "+POST['sponsorId']+" Event ID: "+POST['eventId'], 'occuhunt@gmail.com', EMAIL_MASTERS, fail_silently=False)
        results['success'] = True
    json_results = simplejson.dumps(results)
    return HttpResponse(json_results, mimetype='application/json')