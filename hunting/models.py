from django.db import models
from users.models import User
from fairs.models import Fair

# Create your models here.

class Hunting(models.Model):
	user = models.ForeignKey(User, blank = True, null = True)
	fair = models.ForeignKey(Fair, blank = True, null = True)

	def __unicode__(self):
		return self.user.first_name+":"+self.fair.name