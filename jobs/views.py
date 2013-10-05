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

from social_auth import __version__ as version
from social_auth.utils import setting

def favorites(request):
    """Companies view"""
    favorites_data = Favorite.objects.filter(user__id=request.user.id)
    return render_to_response('favorites.html', {'version': version,'favorites':favorites_data},
                                  RequestContext(request))
