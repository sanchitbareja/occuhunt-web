from django.db import models
import datetime

# Create your models here.

class Fair(models.Model):
	name_of_fair = models.CharField(max_length=512)
	user = models.CharField(max_length=512)

	def __unicode__(self):
		return self.name