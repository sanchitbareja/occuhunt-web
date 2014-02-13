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
from django.core.management.base import BaseCommand, CommandError

from django.core import mail

from occuhunt.settings import EMAIL_MASTERS
from users.models import User

class Command(BaseCommand):
    help = 'Sends new users an email introducing us'

    def handle(self, *args, **options):
        # open mail connections
        connection = mail.get_connection()
        connection.open()

        # defines the templates for sending emails
        template_html = 'emails/new_sign_up.html'
        template_text = 'emails/new_sign_up.txt'

        # all the emails that need to be sent
        emails = []
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        new_users = User.objects.filter(time_created__gt=yesterday)        
        for user in new_users:
            subject = '[Occuhunt] Welcome '+user.first_name+'! Setup your professional profile.'
            from_email = 'occuhunt@gmail.com'
            to_email = user.email

            text_content = render_to_string(template_text, {'name':user.first_name+' '+user.last_name})
            html_content = render_to_string(template_html, {'name':user.first_name+' '+user.last_name})

            msg = mail.EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")
            emails.append(msg)

        # send all the emails at once
        connection.send_messages(emails)
        connection.close()

        self.stdout.write('Successfully sent email to new users!')