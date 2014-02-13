from django.db import models
from users.models import User
from companies.models import Company

# Create your models here.
class CompanyRecruiter(models.Model):
	recruiter = models.ForeignKey(User)
	company = models.ForeignKey(Company)