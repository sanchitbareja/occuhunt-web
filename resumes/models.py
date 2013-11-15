from django.db import models
from django.contrib.auth.models import Group
from users.models import User
import datetime

# Create your models here.
class Resume(models.Model):
	user = models.ForeignKey(User)
	url = models.URLField(max_length=1000)
	timestamp = models.DateTimeField(auto_now_add = True)
	anonymous = models.BooleanField()
	original = models.BooleanField()

	def __unicode__(self):
		return self.name

class Comment(models.Model):
	comment = models.TextField(null = True, blank = True)
	x = models.FloatField(null = True, blank = True)
	y = models.FloatField(null = True, blank = True)
	resume = models.ForeignKey(Resume)
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.comment