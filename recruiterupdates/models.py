from django.db import models
from users.models import User
from fairs.models import Fair
from companies.models import Company

# Create your models here.
class Note(models.Model):
	user = models.ForeignKey(User, related_name='candidate_note')
	recruiter = models.ForeignKey(User, related_name='recruiter_note')
	note = models.TextField()