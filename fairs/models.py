from django.db import models
import datetime

# Create your models here.
class Room(models.Model):
	name = models.CharField(max_length=512)

	def __unicode__(self):
		return self.name

class Fair(models.Model):
	date_start = models.DateField(auto_now=False, auto_now_add=False, default=0)
	date_end = models.DateField(auto_now=False, auto_now_add=False, default=0)
	name = models.CharField(max_length=512)
	rooms = models.ManyToManyField(Room)

	def get_rooms(self):
		return ", ".join([room.name for room in self.rooms.all()])

	def __unicode__(self):
		return self.name