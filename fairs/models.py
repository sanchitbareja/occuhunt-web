from django.db import models
import datetime

# Create your models here.

class Fair(models.Model):
	name = models.CharField(max_length=512)
	venue = models.CharField(max_length=512)
	name = models.DateField(auto_now=False, auto_now_add=False)

	def __unicode__(self):
		return self.name