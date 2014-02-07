from django.db import models
from users.models import User
from fairs.models import Fair
from companies.models import Company

# Create your models here.

STATUS_CATEGORIES = (
	('Applied','Applied'),
	('Reject','Reject'),
	('Interview','Interview'),
	)

class Application(models.Model):
	user = models.ForeignKey(User)
	company = models.ForeignKey(Company)
	fair = models.ForeignKey(Fair)
	status = models.CharField(max_length=512, choices=STATUS_CATEGORIES, default="Applied")
	timestamp = models.DateTimeField(auto_now_add=True)

class Note(models.Model):
	user = models.ForeignKey(User, related_name='candidate_note')
	recruiter = models.ForeignKey(User, related_name='recruiter_note')
	note = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)