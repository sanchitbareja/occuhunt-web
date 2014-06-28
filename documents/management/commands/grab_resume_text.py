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
import os, time, simplejson, datetime, urllib2
from django.core.management.base import BaseCommand, CommandError
from django.core import mail
from django.db.models import Q

from occuhunt.settings import EMAIL_MASTERS
from users.models import User
from documents.models import Document, Visit
import subprocess
import urllib2

class Command(BaseCommand):
    help = 'Updates the Visit table with the location, lat, lng and etc from ip address'

    def handle(self, *args, **options):
        # 1. get all documents that were added within last 1 hour with empty description
        # 2. for each document
        # 3.    fetch document from url
        # 4.    convert to high quality image with imagemagick
        # 5.    get text from high quality image
        # 6.    store text in resume entry as description

        # 1
        hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
        documents_to_update = Document.objects.all()
        # documents_to_update = Document.objects.filter(Q(timestamp__gte=hour_ago), Q(description__isnull=True)| Q(description=''))

        # 2
        for document in documents_to_update:
            try:
                # 3,4 - curl "document.url" | convert -density 300 -depth 8 -quality 85 - tmp.png ; tesseract tmp.png tmp ; cat tmp.txt ; rm tmp.png; rm tmp.txt

                document_url = document.url
                # u = urllib2.urlopen(document_url)
                # localFile = open('temp.pdf', 'w')
                # localFile.write(u.read())

                # print localFile

                # img = Image(filename=localFile.name)
                # img.save(filename='temp.png')

                # localFile.close()

                # print localFile
                subprocess.call('curl --silent \"'+document_url+'\" | convert -density 300 -depth 8 -quality 85 - tmp.png; convert tmp-*.png -append tmp.png ; tesseract tmp.png tmp ; cat tmp.txt ; rm tmp.png; rm tmp-*.png ; rm tmp.txt', shell=True)
                # subprocess.call('rm tmp.*')

            except Exception, e:
                print e

        self.stdout.write('Successfully updated entries in Visit table with locations!')