# Create your views here.
from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django import forms
from django.http import HttpResponseRedirect
from mailer import send_mail, send_html_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
import os, time, simplejson, datetime
from django.core.management.base import BaseCommand, CommandError

from django.core import mail

from occuhunt.settings import EMAIL_MASTERS
from users.models import User

class Command(BaseCommand):
    help = 'Sends new users an email introducing us'

    def handle(self, *args, **options):
        # defines the templates for sending emails
        template_html = 'emails/startup_fair_feedback.html'
        template_text = 'emails/startup_fair_feedback.txt'

        # all the emails that need to be sent
        emails = []
        yesterday = datetime.datetime.now() - datetime.timedelta(days=7)
        new_users = User.objects.filter(time_created__gt=yesterday, recruiter_for__isnull=True)
        for user in new_users:
            subject = 'It was nice meeting you at the startup fair '+user.first_name+'! Stay tuned for application updates!'
            from_email = 'occuhunt@gmail.com'
            to_email = user.email

            text_content = render_to_string(template_text, {'name':user.first_name+' '+user.last_name})
            html_content = render_to_string(template_html, {'name':user.first_name+' '+user.last_name})

            send_html_mail(subject, text_content, html_content, from_email, [to_email])

        self.stdout.write('Successfully sent email to startup fair participants!')