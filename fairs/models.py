from django.db import models
import datetime

# Create your models here.
class Room(models.Model):
	name = models.CharField(max_length=512)

	def __unicode__(self):
		return self.name

class Fair(models.Model):
	time_start = models.DateTimeField(auto_now=False, auto_now_add=False)
	time_end = models.DateTimeField(auto_now=False, auto_now_add=False)
	name = models.CharField(max_length=512)
	rooms = models.ManyToManyField(Room)
	logo = models.URLField(max_length=512, null=True, blank=True)

	def get_rooms(self):
		return ", ".join([room.name for room in self.rooms.all()])

	def __unicode__(self):
		return self.name