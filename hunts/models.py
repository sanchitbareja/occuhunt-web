from django.db import models
from users.models import User
from fairs.models import Fair
from companies.models import Company

# Create your models here.
class Hunt(models.Model):
	user = models.ForeignKey(User)
	fair = models.ForeignKey(Fair)

class Resumedrop(models.Model):
	user = models.ForeignKey(User)
	fair = models.ForeignKey(fair)
	company = models.ForeignKey(Company)