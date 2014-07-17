from django.db import models
from users.models import User
from fairs.models import Fair
from companies.models import Company
from resumes.models import Resume
from jobs.models import Job

# signals
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# misc
import datetime
from mailer import send_mail, send_html_mail
from occuhunt.settings import EMAIL_MASTERS
from django.template.loader import render_to_string

COMPANY_CATEGORY = (
	(1, 'Top 25'),
	(2, 'Fortune 500'),
	(3, 'Startup'),
	(4, 'Other'),
	)

SALARY_RANGE_CHOICES = (
	(1,'20k-30k'),
	(2,'30k-40k'),
	(3,'40k-50k'),
	(4,'50k-60k'),
	(5,'60k-70k'),
	(6,'70k-80k'),
	(7,'80k-100k'),
	(8,'100k-120k'),
	(9,'120k-140k'),
	(10,'140k-160k'),
	(11,'160k-180k'),
	(12,'180k-200k'),
	(13,'200k-250k'),
	(14,'250k+'),
	(15,'NDA'),
	)

OFFER_DEADLINE_CHOICES = (
	(1, 'In 3 days'),
	(2, 'In 7 days'),
	(3, 'In 14 days'),
	(4, 'In 28 days'),
	(5, 'I have time'),
	)

class Offer(models.Model):
	user = models.ForeignKey(User)
	company_from_text = models.CharField(max_length=300)
	company_from = models.ForeignKey(Company, null=True, blank=True)
	company_category = models.SmallIntegerField(choices=COMPANY_CATEGORY, default=1)
	number_of_offers = models.SmallIntegerField(null=True, blank=True)
	salary_range = models.SmallIntegerField(choices=SALARY_RANGE_CHOICES, default=15)
	offer_deadline = models.SmallIntegerField(choices=OFFER_DEADLINE_CHOICES, default=3)
	interested_in_startups = models.BooleanField(default=False)
	interested_in_corps = models.BooleanField(default=True)
	companies_considering = models.TextField()
	approved = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
