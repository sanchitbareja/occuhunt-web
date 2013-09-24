from django.db import models
from users.models import User
from companies.models import Company

# Create your models here.
class Favorite(models.Model):
	user = models.ForeignKey(User, blank = True, null = True)
	company = models.ForeignKey(Company, blank = True, null = True)

	def __unicode__(self):
		return unicode("Fav")