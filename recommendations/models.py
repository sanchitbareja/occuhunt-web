from django.db import models
from django.contrib.auth.models import Group
from users.models import User
import datetime

# # Create your models here.
# class Recommendation(models.Model):
# 	recommender = models.ForeignKey(User, related_name = "recommender")
# 	recommendee = models.ForeignKey(User, related_name = "recommendee")
# 	relationship = models.CharField(max_length=256, null=True, blank=True)
# 	at = models.CharField(max_length=1000, null=True, blank=True)
# 	answer1 = models.TextField(null=True, blank=True)
# 	answer2 = models.TextField(null=True, blank=True)
# 	answer3 = models.TextField(null=True, blank=True)

# 	def __unicode__(self):
# 		return str(self.recommendee)+":"+str(self.recommender)

class Request(models.Model):
	request_from = models.CharField(max_length=256, null=True, blank=True)
	request_to = models.CharField(max_length=256, null=True, blank=True)
	relationship = models.CharField(max_length=256, null=True, blank=True)
	project = models.CharField(max_length=1000, null=True, blank=True)
	message = models.TextField(null=True, blank=True)
	deadline = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, blank=True)

	def __unicode__(self):
		return str(self.request_from)+":"+str(self.request_to)