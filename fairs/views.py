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

from resumes.models import Resume

def create_fair(request):
    """View to automatically create fairs"""
    return render_to_response('create_fair_map.html', {},
                                  RequestContext(request))

def StartupCareerFairSpring2014View(request):
	"""View to StartupCareerFairSpring2014 """
	print request.user
	if request.user.is_anonymous():
		# if it's anonymous user
		return render_to_response('CareerFairs/UCBerkeley/StartupCareerFairSpring2014.html', {'resume_url':False}, RequestContext(request))
	else:
		resume = Resume.objects.filter(user=request.user, showcase=True, original=False).order_by('-timestamp')
		if len(resume) > 0:
			# if user has a resume - yay!
			resume = resume[0]
			return render_to_response('CareerFairs/UCBerkeley/StartupCareerFairSpring2014.html', {'resume_url':resume.url}, RequestContext(request))
		else:
			# if user doesn't have a resume on file, boo :(
			resume = None
			return render_to_response('CareerFairs/UCBerkeley/StartupCareerFairSpring2014.html', {'resume_url':False}, RequestContext(request))


def ISchoolInfoCampView(request):
	"""View to ISchoolInfoCamp """
	print request.user
	if request.user.is_anonymous():
		# if it's anonymous user
		return render_to_response('CareerFairs/UCBerkeley/InfoCampSpring2014.html', {'resume_url':False}, RequestContext(request))
	else:
		resume = Resume.objects.filter(user=request.user, showcase=True, original=False).order_by('-timestamp')
		if len(resume) > 0:
			# if user has a resume - yay!
			resume = resume[0]
			return render_to_response('CareerFairs/UCBerkeley/InfoCampSpring2014.html', {'resume_url':resume.url}, RequestContext(request))
		else:
			# if user doesn't have a resume on file, boo :(
			resume = None
			return render_to_response('CareerFairs/UCBerkeley/InfoCampSpring2014.html', {'resume_url':False}, RequestContext(request))


def PBLCareerFairSpring2014View(request):
	"""View to ISchoolInfoCamp """
	print request.user
	if request.user.is_anonymous():
		# if it's anonymous user
		return render_to_response('CareerFairs/UCBerkeley/PBLCareerFairSpring2014.html', {'resume_url':False}, RequestContext(request))
	else:
		resume = Resume.objects.filter(user=request.user, showcase=True, original=False).order_by('-timestamp')
		if len(resume) > 0:
			# if user has a resume - yay!
			resume = resume[0]
			return render_to_response('CareerFairs/UCBerkeley/PBLCareerFairSpring2014.html', {'resume_url':resume.url}, RequestContext(request))
		else:
			# if user doesn't have a resume on file, boo :(
			resume = None
			return render_to_response('CareerFairs/UCBerkeley/PBLCareerFairSpring2014.html', {'resume_url':False}, RequestContext(request))


def Dropin357View(request):
	"""View to ISchoolInfoCamp """
	print request.user
	if request.user.is_anonymous():
		# if it's anonymous user
		return render_to_response('CareerFairs/UCBerkeley/357April92014.html', {'resume_url':False}, RequestContext(request))
	else:
		resume = Resume.objects.filter(user=request.user, showcase=True, original=False).order_by('-timestamp')
		if len(resume) > 0:
			# if user has a resume - yay!
			resume = resume[0]
			return render_to_response('CareerFairs/UCBerkeley/357April92014.html', {'resume_url':resume.url}, RequestContext(request))
		else:
			# if user doesn't have a resume on file, boo :(
			resume = None
			return render_to_response('CareerFairs/UCBerkeley/357April92014.html', {'resume_url':False}, RequestContext(request))

def Dropin3572View(request):
	"""View to ISchoolInfoCamp """
	print request.user
	if request.user.is_anonymous():
		# if it's anonymous user
		return render_to_response('CareerFairs/UCBerkeley/357April162014.html', {'resume_url':False}, RequestContext(request))
	else:
		resume = Resume.objects.filter(user=request.user, showcase=True, original=False).order_by('-timestamp')
		if len(resume) > 0:
			# if user has a resume - yay!
			resume = resume[0]
			return render_to_response('CareerFairs/UCBerkeley/357April162014.html', {'resume_url':resume.url}, RequestContext(request))
		else:
			# if user doesn't have a resume on file, boo :(
			resume = None
			return render_to_response('CareerFairs/UCBerkeley/357April162014.html', {'resume_url':False}, RequestContext(request))

