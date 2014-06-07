from django.db import models
from django.contrib.auth.models import Group
from users.models import User
import datetime

# signals
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# misc
import datetime
from mailer import send_mail, send_html_mail
from occuhunt.settings import EMAIL_MASTERS
from django.template.loader import render_to_string

# variables
DOCUMENT_CHOICES = (
	(1, 'Resume'),
	(2, 'CV'),
	(3, 'Portfolio'))

VISIT_CHOICES = (
	(1, 'Visit'),
	(2, 'Download'),
	(3, 'Clicked Link'))

# Create your models here.
class Document(models.Model):
	user = models.ForeignKey(User)
	document_type = models.PositiveSmallIntegerField(choices=DOCUMENT_CHOICES)
	image_url = models.URLField(max_length=1000)
	url = models.URLField(max_length=1000)
	unique_hash = models.CharField(max_length=10, unique=True)
	delete = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add = True)

	def __unicode__(self):
		return str(self.user)+":"+self.url


class Link(models.Model):
	user = models.ForeignKey(User)
	link_name = models.CharField(max_length=255)
	url = models.URLField(max_length=1000)
	delete = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add = True)

	def __unicode__(self):
		return str(self.user)+":"+self.link_name+" - "+self.url


class Visit(models.Model):
	document = models.ForeignKey(Document, blank=True, null=True)
	ip_address = models.CharField(max_length=128)
	visit_type = models.PositiveSmallIntegerField(choices=VISIT_CHOICES)
	link = models.ForeignKey(Link, blank=True, null=True)
	country_code = models.CharField(max_length=10, null=True, blank=True)
	country_name = models.CharField(max_length=2056, null=True, blank=True)
	region_code = models.CharField(max_length=10, null=True, blank=True)
	region_name = models.CharField(max_length=2056, null=True, blank=True)
	city = models.CharField(max_length=2056, null=True, blank=True)
	zipcode = models.CharField(max_length=255, null=True, blank=True)
	lat = models.FloatField(null=True, blank=True)
	lng = models.FloatField(null=True, blank=True)
	metro_code = models.CharField(max_length=255, null=True, blank=True)
	area_code = models.CharField(max_length=255, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add = True)

