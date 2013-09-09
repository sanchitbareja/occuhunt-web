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

def home(request):
    """Home view"""
    return render_to_response('index.html', {'version': version},
                                  RequestContext(request))


def companies(request):
    """Companies view"""
    return render_to_response('companies.html', {'version': version},
                                  RequestContext(request))
