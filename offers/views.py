from django.template import Context, RequestContext
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django import forms
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import os, time, simplejson
from datetime import datetime, timedelta, time
from django.db.models import Avg

from users.models import Major, Degree
from resumes.models import Resume
from offers.models import Offer

# Create your views here.
def offrhunt_handler(request):
	""" View to the offrhunt """
	# get offrhunt detail
	print "offrhunt"
	try:
		time_now = datetime.now()
		if request.user.is_anonymous():
			# if it's anonymous user
			return render_to_response('base/offrhunt_template.html', {'resume_url':False, 'time_now':time_now}, RequestContext(request))
		else:
			current_offer = Offer.objects.filter(user=request.user)
			resume = Resume.objects.filter(user=request.user, showcase=True, original=False).order_by('-timestamp')
			majors = Major.objects.all()
			degree_types = Degree.objects.all()
			if len(current_offer) > 0:
				current_offer = True
			else:
				current_offer = False
			if len(resume) > 0:
				# if user has a resume - yay!
				resume = resume[0]
				return render_to_response('base/offrhunt_template.html', {'resume_url':resume.url, 'majors':majors, 'degree_types':degree_types, 'time_now':time_now, 'current_offer': current_offer}, RequestContext(request))
			else:
				# if user doesn't have a resume on file, boo :(
				resume = None
				return render_to_response('base/offrhunt_template.html', {'resume_url':False, 'majors':majors, 'degree_types':degree_types, 'time_now':time_now, 'current_offer': current_offer}, RequestContext(request))
	except:
		raise Http404()