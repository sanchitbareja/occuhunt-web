from django.db import models
from companies.models import Company
from jobs.models import Job
import datetime

FITTING_LABEL_CHOICES = (
	(1, 'Wall'),
	(2, 'Entrance'),
	(3, 'Exit'),
	)

FITTING_FUNCTION_CHOICES = (
	(1, 'Linear'),
	(2, 'Qudratic'),
	(3, 'Top Circle'),
	(4, 'Bottom Circle'),
	)

EVENT_TYPE_CHOICES = (
	(1, 'Infosession'),
	(2, '357'),
	(3, 'Career Fair'),
	(4, 'Roundtable'),
	(5, 'Networking Mixer'),
	)

# Create your models here.
class Location(models.Model):
	name = models.CharField(max_length=512)
	lat = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
	lng = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)

class Fitting(models.Model):
	x1 = models.PositiveIntegerField()
	y1 = models.PositiveIntegerField()
	x2 = models.PositiveIntegerField()
	y2 = models.PositiveIntegerField()
	fn = models.PositiveIntegerField(max_length=512, null=True, blank=True, choices=FITTING_FUNCTION_CHOICES)
	label = models.PositiveIntegerField(max_length=512, null=True, blank=True, choices=FITTING_LABEL_CHOICES)
	image = models.URLField(max_length=512, null=True, blank=True)

	def __unicode__(self):
		return FITTING_LABEL_CHOICES[self.label-1][1]

class Table(models.Model):
	x = models.PositiveIntegerField()
	y = models.PositiveIntegerField()
	width = models.PositiveIntegerField()
	height = models.PositiveIntegerField()
	rotation = models.PositiveIntegerField(default=90)
	company = models.ForeignKey(Company)

	def __unicode__(self):
		return self.company.name

class Map(models.Model):
	tables = models.ManyToManyField(Table)
	fittings = models.ManyToManyField(Fitting)

class Room(models.Model):
	name = models.CharField(max_length=512)
	lat = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
	lng = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
	map = models.ForeignKey(Map, blank=True, null=True)

	def __unicode__(self):
		return self.name

class Fair(models.Model):
	time_start = models.DateTimeField(auto_now=False, auto_now_add=False)
	time_end = models.DateTimeField(auto_now=False, auto_now_add=False)
	name = models.CharField(max_length=512)
	venue = models.CharField(max_length=512)
	rooms = models.ManyToManyField(Room)
	logo = models.URLField(max_length=512, null=True, blank=True)
	resume_drop = models.BooleanField(default=False)
	organizers = models.ManyToManyField(Company, related_name='organizers', null=True, blank=True)
	sponsors = models.ManyToManyField(Company, related_name='sponsors', null=True, blank=True)
	event_type = models.PositiveIntegerField(max_length=3, choices=EVENT_TYPE_CHOICES, default=1)
	thumbnail = models.URLField(max_length=1024, null=True, blank=True)
	location = models.ForeignKey(Location, null=True, blank=True)

	def get_rooms(self):
		return ", ".join([room.name for room in self.rooms.all()])

	def __unicode__(self):
		return self.name

class Infosession(models.Model):
	name = models.CharField(max_length=512)
	company = models.ForeignKey(Company)
	banner = models.URLField(max_length=1024, null=True, blank=True)
	fair = models.OneToOneField(Fair, related_name='infosession')

class ThreeFiveSeven(models.Model):
	name = models.CharField(max_length=512)
	companies = models.ManyToManyField(Company)
	fair = models.OneToOneField(Fair, related_name='threeFiveSeven')
