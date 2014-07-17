# Create your views here.
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

from notifications.models import Notification
from applications.models import Application

@login_required
def showcase_notifications(request):
	"""
	show the last 50 notifications to the user
	- if more than 50 unread notifications, show all
	- if less than 50 unread notifications, show up to 50 notifications only
	"""
	# new notifications for the people
	old_notifications = Notification.objects.filter(user=request.user, receiver=1, read_receipt=True).order_by('-timestamp')[0:50]
	unread_notifications = Notification.objects.filter(user=request.user, receiver=1, read_receipt=False).order_by('-timestamp')
	for notification in unread_notifications:
		notification.read_receipt = True
		notification.save()
	return render_to_response('showcase_notifications.html', {'unread_notifications':unread_notifications, 'old_notifications':old_notifications}, RequestContext(request))


@login_required
def showcase_applications(request):
	"""
	show the applications statuses
	- user
	- company
	- fair
	- status
	"""
	# new notifications for the people
	applications = Application.objects.filter(user=request.user).order_by('-timestamp')
	return render_to_response('showcase_applications.html', {'applications':applications}, RequestContext(request))
