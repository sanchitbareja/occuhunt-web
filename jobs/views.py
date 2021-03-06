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

from favorites.models import Favorite

def favorites(request):
    """Companies view"""
    favorites_data = Favorite.objects.filter(user__id=request.user.id)
    return render_to_response('favorites.html', {'favorites':favorites_data, 'companies_and_favorites_link':True},
                                  RequestContext(request))
def apply_jobs(request):
    """Application form for companies"""
    return render_to_response('apply.html', {"apply_link":True}, RequestContext(request))

def match_jobs(request):
    """Match people with companies"""
    return render_to_response('match.html', {"match_link":True}, RequestContext(request))