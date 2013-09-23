# Create your views here.
from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django import forms
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
import os, time, simplejson
from datetime import datetime, timedelta, time
from occuhunt.settings import EMAIL_MASTERS

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('/')

def login_error(request):
	print request
	return redirect('/')

def feedback_form(request):
    """post feedback form and send email"""
    results = {'success':False}
    if(request.method == u'POST'):
        POST = request.POST
        send_mail('[Occuhunt] Someone just left you a feedback!', POST['feedback']+" REPLY TO EMAIL: "+POST['replyToEmail'], 'occuhunt@gmail.com', EMAIL_MASTERS, fail_silently=False)
        results['success'] = True
    json_results = simplejson.dumps(results)
    return HttpResponse(json_results, mimetype='application/json')