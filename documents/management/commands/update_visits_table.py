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
from documents.models import Visit

class Command(BaseCommand):
    help = 'Updates the Visit table with the location, lat, lng and etc from ip address'

    def handle(self, *args, **options):
        # 1. get all Visit entries that have to be updates - without country_code
        # 2. iterate through each entry and get their info through this: http://freegeoip.net/json/192.168.0.1
        # 3.    in each entry, update the information
        # 4.    save each entry

        # 1
        visits_to_update = Visit.objects.filter(Q(country_code__isnull=True)|Q(country_code=''))

        # 2
        for visit in visits_to_update:
            try:
                url = 'http://freegeoip.net/json/'+visit.ip_address
                json_response = urllib2.urlopen(url).read()
                response = simplejson.loads(json_response)

                print response

                # 3. update visit with ip address info
                visit.country_code = response['country_code']
                visit.country_name = response['country_name']
                visit.region_code = response['region_code']
                visit.region_name = response['region_name']
                visit.city = response['city']
                visit.zipcode = response['zipcode']
                visit.lat = response['latitude']
                visit.lng = response['longitude']
                visit.metro_code = response['metro_code']
                visit.area_code = response['area_code']

                # 4
                visit.save()
            except Exception, e:
                print e

        self.stdout.write('Successfully updated entries in Visit table with locations!')