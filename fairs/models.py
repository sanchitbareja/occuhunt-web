from django.db import models
import datetime

# Create your models here.

class Fair(models.Model):
	venue = models.CharField(max_length=512)
	date_start = models.DateField(auto_now=False, auto_now_add=False, default=0)
	date_end = models.DateField(auto_now=False, auto_now_add=False, default=0)
	name = models.CharField(max_length=512)

	def __unicode__(self):
		return self.name