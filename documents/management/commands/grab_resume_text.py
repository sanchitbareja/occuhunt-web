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
    help = 'Updates the Document table with the description of the document'

    def handle(self, *args, **options):
        # 1. get all documents that were added within last 1 hour with empty description
        # 2. for each document
        # 3.    fetch document from url
        # 4.    convert to high quality image with imagemagick
        # 5.    get text from high quality image
        # 6.    store text in resume entry as description
        # 7.    Clean up and remove temp files

        # 1
        aday_ago = datetime.datetime.now() - datetime.timedelta(hours=24)
        # documents_to_update = Document.objects.all()
        documents_to_update = Document.objects.filter(Q(timestamp__gte=aday_ago), Q(description__isnull=True)| Q(description=''))

        # 2
        for document in documents_to_update:
            try:
                # 3,4 and part of 5
                document_url = document.url
                unique_hash = document.unique_hash
                subprocess.call('curl --silent \"'+document_url+'\" | convert -density 300 -depth 8 -quality 85 - '+unique_hash+'.png;', shell=True)
                subprocess.call('convert '+unique_hash+'-*.png -append '+unique_hash+'.png;', shell=True)
                subprocess.call('tesseract '+unique_hash+'.png '+unique_hash+';', shell=True)

                print "check 1"

                # 5
                text_file = open(''+unique_hash+'.txt','r')
                document_text = text_file.read()
                text_file.close()

                print "check 2"

                # 6
                document.description = document_text
                document.save()

                print "check 3"

                # 7. remove temp files
                subprocess.call('rm '+unique_hash+'*')

                print "check 4"

            except Exception, e:
                print e

        self.stdout.write('Successfully updated documents with descriptions!')