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
from documents.models import Document, Visit, Link
from fairs.models import Fair, ThreeFiveSeven, Infosession

def create_fair(request):
	"""View to automatically create fairs"""
	return render_to_response('create_fair_map.html', {},
								  RequestContext(request))

def all_events(request):
	"""View all events for a specific network"""
	# if user is logged in
		# Get network of the request
		# get events related to event grouped by month
		# if lesser than 10 events in the network, show all events in the past 6 months as well
	# if user is not not logged in
		# get all events in the past six months grouped by month

	today = datetime.today()
	sixMonthsAgo = today - timedelta(days=178)
	all_events = Fair.objects.filter(time_start__gt=sixMonthsAgo).order_by('-time_start')

	# center of map coordinates
	lat_avg = all_events.aggregate(Avg('location__lat'))
	lng_avg = all_events.aggregate(Avg('location__lng'))
	print lat_avg
	print lng_avg

	return render_to_response('events.html', {'events':all_events, 'lat_avg':lat_avg['location__lat__avg'], 'lng_avg':lng_avg['location__lng__avg']}, RequestContext(request))

def three_five_seven_handler(request, three_five_seven_id):
	""" View to the 357 event """
	# get 357 detail
	try:
		event = ThreeFiveSeven.objects.get(id=int(three_five_seven_id))
		time_now = datetime.now()
		if request.user.is_authenticated():
			# if logged in
			resumes = Document.objects.filter(user=request.user, document_type=1, delete=False)
			cvs = Document.objects.filter(user=request.user, document_type=2, delete=False)
			portfolios = Document.objects.filter(user=request.user, document_type=3, delete=False)
			links = Link.objects.filter(user=request.user, delete=False)

			majors = Major.objects.all()
			degree_types = Degree.objects.all()

			data_to_send = {
				'event':event,
				'majors':majors,
				'degree_types':degree_types,
				'time_now':time_now,
				'resumes': resumes,
				'cvs': cvs,
				'portfolios': portfolios,
				'links': links
			}
			return render_to_response('base/357v2.html', data_to_send, RequestContext(request))
		else:
			# if anonymous user
			data_to_send = {
				'event':event,
				'time_now':time_now,
				'resumes': None,
				'cvs': None,
				'portfolios': None,
				'links': None
			}
			return render_to_response('base/357v2.html', data_to_send, RequestContext(request))
	except Exception, e:
		print e
		raise Http404()

def infosession_handler(request, company, infosession_id):
	""" View to the infosession event """
	# get infosession detail
	try:
		event = Infosession.objects.get(id=int(infosession_id))
		time_now = datetime.now()
		if request.user.is_anonymous():
			# if it's anonymous user
			return render_to_response('base/infosession_template.html', {'event':event, 'resume_url':False, 'time_now':time_now}, RequestContext(request))
		else:
			resume = Resume.objects.filter(user=request.user, showcase=True, original=False).order_by('-timestamp')
			majors = Major.objects.all()
			degree_types = Degree.objects.all()
			if len(resume) > 0:
				# if user has a resume - yay!
				resume = resume[0]
				return render_to_response('base/infosession_template.html', {'event':event, 'resume_url':resume.url, 'majors':majors, 'degree_types':degree_types, 'time_now':time_now}, RequestContext(request))
			else:
				# if user doesn't have a resume on file, boo :(
				resume = None
				return render_to_response('base/infosession_template.html', {'event':event, 'resume_url':False, 'majors':majors, 'degree_types':degree_types, 'time_now':time_now}, RequestContext(request))	
	except:
		raise Http404()

def career_fair_handler(request, event_name, fair_id):
	""" View to the career fair event """
	try:
		event = Fair.objects.get(id=int(fair_id))
		career_fair_render = 'CareerFairs/UCBerkeley/'+str(fair_id)+'.html'
		time_now = datetime.now()
		if request.user.is_authenticated():
			# if logged in
			resumes = Document.objects.filter(user=request.user, document_type=1, delete=False)
			cvs = Document.objects.filter(user=request.user, document_type=2, delete=False)
			portfolios = Document.objects.filter(user=request.user, document_type=3, delete=False)
			links = Link.objects.filter(user=request.user, delete=False)

			majors = Major.objects.all()
			degree_types = Degree.objects.all()

			data_to_send = {
				'event':event,
				'majors':majors,
				'degree_types':degree_types,
				'time_now':time_now,
				'resumes': resumes,
				'cvs': cvs,
				'portfolios': portfolios,
				'links': links
			}
			return render_to_response(career_fair_render, data_to_send, RequestContext(request))
		else:
			# if anonymous user
			data_to_send = {
				'event':event,
				'time_now':time_now,
				'resumes': None,
				'cvs': None,
				'portfolios': None,
				'links': None
			}
			return render_to_response(career_fair_render, data_to_send, RequestContext(request))
	except Exception, e:
		print e
		raise Http404()

