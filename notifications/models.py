from django.db import models
from users.models import User
from fairs.models import Fair
from companies.models import Company

# signals
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# Create your models here.

NOTIFICATION_CATEGORIES = (
	(1,'Viewed Profile'),
	(2,'Downloaded Resume'),
	(3,'Rejected'),
	(4,'To Call For Interview'),
	)

RECEIVER_CHOICES = (
	(1,'Student'),
	(2,'Company'),
	)

class Notification(models.Model):
	user = models.ForeignKey(User)
	company = models.ForeignKey(Company)
	receiver = models.SmallIntegerField(choices=RECEIVER_CHOICES, default=1)
	notification = models.SmallIntegerField(choices=NOTIFICATION_CATEGORIES, default=1)
	read_receipt = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True)