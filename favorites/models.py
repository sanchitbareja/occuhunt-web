from django.db import models
from users.models import User
from companies.models import Company

# Create your models here.

FAVORITE_CATEGORIES = (
	('Uncategorized','Uncategorized'),
	('Applied', 'Applied'),
	('Interviewing', 'Interviewing'),
	('Offered', 'Offered'),
	)

class Favorite(models.Model):
	user = models.ForeignKey(User, blank = True, null = True)
	company = models.ForeignKey(Company, blank = True, null = True)
	category = models.CharField(max_length=256, null=True, blank=True, choices=FAVORITE_CATEGORIES, default="Uncategorized")
	note = models.TextField(default='')

	def __unicode__(self):
		return unicode("Fav")