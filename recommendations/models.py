from django.db import models
from django.contrib.auth.models import Group
from users.models import User
import datetime

# Create your models here.
class Recommendation(models.Model):
	recommender = models.ForeignKey(User, related_name = "recommender")
	recommendee = models.ForeignKey(User, related_name = "recommendee")

	def __unicode__(self):
		return self.name