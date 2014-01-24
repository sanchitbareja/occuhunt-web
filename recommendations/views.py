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

from recommendations.models import Recommendation, Request

from social_auth import __version__ as version
from social_auth.utils import setting

@login_required
def recommendation_main(request):
    """
    View to automatically create fairs
    """
    # get current user_id
    # get linkedin uid for this user_id
    # get recommendations for this guy
	# jumble these recs up
	# get recommendations by this guy
    return render_to_response('recommendation.html', {'version': version}, RequestContext(request))

@login_required
def recommendation_new(request, linkedin_uid):
	"""
	Create a new recommendation 
	"""
	print linkedin_uid
	print request.user
	print request.user.linkedin_uid
	return render_to_response('recommendation_new.html', {'version': version, 'recommendation_for':linkedin_uid, 'recommendation_by':request.user.linkedin_uid}, RequestContext(request))

@login_required
def recommendation_requests(request):
	"""
	Lists all the outstanding recommendation requests
	"""
	# get current user_id
	print request.user
	print request.user.linkedin_uid
	print Request.objects.filter(request_to=request.user.linkedin_uid)
	# get linkedin uid for this user_id
	# get requests for this person
	return render_to_response('recommendation_requests.html', {'version': version, 'recommendation_requests':Request.objects.filter(request_to=request.user.linkedin_uid)}, RequestContext(request))

@login_required
def recommendation_requests_new(request):
	"""
	Create a new request for recommendation
	"""
	return render_to_response('recommendation_requests_new.html', {'version': version}, RequestContext(request))