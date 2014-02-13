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
from resumes.models import Resume

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
	recommendations_for_me = Recommendation.objects.filter(recommendation_to=request.user.linkedin_uid)
	resume = Resume.objects.filter(user=request.user, showcase=True, original=False).order_by('-timestamp')
	if len(resume) > 0:
		resume = resume[0]
	else:
		resume = None
	# number of requests he has
	requests_number = Request.objects.filter(request_to=request.user.linkedin_uid, replied=False).count()
	return render_to_response('recommendation.html', {'version': version, 'requests_number':requests_number, 'recommendations_for_me':recommendations_for_me, 'user_linkedin_uid':request.user.linkedin_uid, 'resume':resume}, RequestContext(request))

@login_required
def recommendation_new(request, linkedin_uid):
	"""
	Create a new recommendation 
	"""
	requests_number = Request.objects.filter(request_to=request.user.linkedin_uid, replied=False).count()
	return render_to_response('recommendation_new.html', {'version': version, 'requests_number':requests_number, 'recommendation_for':linkedin_uid, 'recommendation_by':request.user.linkedin_uid}, RequestContext(request))

@login_required
def recommendation_new_with_request(request, linkedin_uid, request_id):
	"""
	Create a new recommendation
	"""
	# check if request_id even exists in the database -> else redirect to normal recommendation with linkedin_uid
	response_to = Request.objects.filter(id=request_id, request_from=linkedin_uid)
	if len(response_to):
		# number of requests he has
		requests_number = Request.objects.filter(request_to=request.user.linkedin_uid, replied=False).count()
		return render_to_response('recommendation_new.html', {'version': version, 'requests_number':requests_number, 'recommendation_for':linkedin_uid, 'recommendation_by':request.user.linkedin_uid, 'request_id':response_to[0].id}, RequestContext(request))
	else:
		return redirect('recommendation_new', linkedin_uid)

@login_required
def recommendation_requests(request):
	"""
	Lists all the outstanding recommendation requests
	"""
	# get current user_id
	recommendation_requests = Request.objects.filter(request_to=request.user.linkedin_uid, replied=False)
	# get linkedin uid for this user_id
	# get requests for this person
	# number of requests he has
	requests_number = Request.objects.filter(request_to=request.user.linkedin_uid, replied=False).count()
	return render_to_response('recommendation_requests.html', {'version': version, 'requests_number':requests_number, 'recommendation_requests':recommendation_requests}, RequestContext(request))

@login_required
def recommendation_requests_new(request):
	"""
	Create a new request for recommendation
	"""
	# number of requests he has
	requests_number = Request.objects.filter(request_to=request.user.linkedin_uid, replied=False).count()
	return render_to_response('recommendation_requests_new.html', {'version': version, 'requests_number':requests_number}, RequestContext(request))

@login_required
def recommendation_analytics(request):
	"""
	Create a new request for recommendation
	"""
	# number of requests he has
	requests_number = Request.objects.filter(request_to=request.user.linkedin_uid, replied=False).count()
	return render_to_response('recommendation_requests_new.html', {'version': version, 'requests_number':requests_number}, RequestContext(request))