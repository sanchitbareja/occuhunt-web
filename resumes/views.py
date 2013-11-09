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

from social_auth import __version__ as version
from social_auth.utils import setting

def resume_feed(request):
    """Resume feed view"""
    return render_to_response('resume_feed.html', {'version': version}, RequestContext(request))