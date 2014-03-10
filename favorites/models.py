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
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __unicode__(self):
		return unicode(self.user.first_name + ':' + self.company.name)

	class Meta:
		# each user can only favorite a company once
		unique_together = (('user','company'),)