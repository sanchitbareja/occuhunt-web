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

# Create your models here.
class Event(models.Model):
	name = models.CharField(max_length=512)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	time_start = models.DateTimeField(auto_now=False, auto_now_add=False)
	time_end = models.DateTimeField(auto_now=False, auto_now_add=False)

class Fitting(models.Model):
	x1 = models.PositiveIntegerField()
	y1 = models.PositiveIntegerField()
	x2 = models.PositiveIntegerField()
	y2 = models.PositiveIntegerField()
	fn = models.CharField(max_length=512, null=True, blank=True, choices=FITTING_FUNCTION_CHOICES)
	label = models.CharField(max_length=512, null=True, blank=True, choices=FITTING_LABEL_CHOICES)
	image = models.URLField(max_length=512, null=True, blank=True)

class Table(models.Model):
	x = models.PositiveIntegerField()
	y = models.PositiveIntegerField()
	width = models.PositiveIntegerField()
	height = models.PositiveIntegerField()
	rotation = models.PositiveIntegerField(default=90)
	company = models.ForeignKey(Company)

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
	event = models.ForeignKey(Event, blank=True, null=True)
	resume_drop = models.BooleanField(default=False)
	organizers = models.ManyToManyField(Company, related_name='organizers', null=True, blank=True)
	sponsors = models.ManyToManyField(Company, related_name='sponsors', null=True, blank=True)
	job = models.ManyToManyField(Job, null=True, blank=True)

	def get_rooms(self):
		return ", ".join([room.name for room in self.rooms.all()])

	def __unicode__(self):
		return self.name