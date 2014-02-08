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

from social_auth import __version__ as version
from social_auth.utils import setting

def create_fair(request):
    """View to automatically create fairs"""
    return render_to_response('create_fair_map.html', {'version': version},
                                  RequestContext(request))

def StartupCareerFairSpring2014View(request):
	"""View to StartupCareerFairSpring2014V """
	return render_to_response('CareerFairs/UCBerkeley/StartupCareerFairSpring204.html', {'version':version}, RequestContext(request))