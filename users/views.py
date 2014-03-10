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

# Create your views here.
def get_user_network(request):
	"""
	1. decode token
	2. get network, user_id, email
	3. complete partial_pipeline
	"""
	if request.method == 'POST':
		request.session['verified_email'] = request.POST.get('verified_email_address')
		request.session['school_network'] = request.POST.get('verified_network')
		request.session['email_identifier'] = request.POST.get('email_identifier')
		backend = request.session['partial_pipeline']['backend']
		return redirect('social:complete', backend=backend)
	return render_to_response('registeration/get_network.html', {}, RequestContext(request))

def verify_user_network(request):
	"""
	1. decode token
	2. get network, user_id, email
	3. complete partial_pipeline
	"""
	pass