from django.db import models
from users.models import User
from fairs.models import Fair
from companies.models import Company
from hunts.models import Hunt

# signals
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# Create your models here.

STATUS_CATEGORIES = (
	(1,'Applied'),
	(2,'Reject'),
	(3,'Interview'),
	)

POSITION_CATEGORIES = (
	('Software Engineering','Software Engineering'),
	('Accountant','Accountant'),
	('Product Manager','Product Manager'),
	('Other','Other')
	)

class Application(models.Model):
	user = models.ForeignKey(User)
	company = models.ForeignKey(Company)
	fair = models.ForeignKey(Fair)
	status = models.SmallIntegerField(choices=STATUS_CATEGORIES, default=1)
	position = models.CharField(max_length=512, default="Other")
	timestamp = models.DateTimeField(auto_now_add=True)

class Note(models.Model):
	user = models.ForeignKey(User, related_name='candidate_note')
	recruiter = models.ForeignKey(User, related_name='recruiter_note')
	note = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)


def auto_hunt(sender, instance, **kwargs):
	"""
	auto create a unique 'hunt' for the person
	"""
	# get user and fair
	# check if user has already checked in for that fair
	# 	if he has - do nothing
	# 	else create a hunt entry for him
	user = instance.user
	fair = instance.fair
	existing_hunt = Hunt.objects.filter(user=user, fair=fair)
	if not len(existing_hunt) > 0:
		new_hunt = Hunt(user=user, fair=fair)
		new_hunt.save()

post_save.connect(auto_hunt, sender=Application)