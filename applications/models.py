from django.db import models
import datetime

# Create your models here.

# Create your models here.
class CompanyType(models.Model):
	type = models.CharField(max_length = 256)

	def __unicode__(self):
		return self.type