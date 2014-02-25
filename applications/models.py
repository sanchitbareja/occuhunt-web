from django.db import models
from users.models import User
from fairs.models import Fair
from companies.models import Company
from hunts.models import Hunt
from resumes.models import Resume

# signals
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# misc
import datetime
from mailer import send_mail, send_html_mail
from occuhunt.settings import EMAIL_MASTERS
from django.template.loader import render_to_string

# Create your models here.

STATUS_CATEGORIES = (
	(1,'Applied'),
	(2,'Interacted With'),
	(3,'Rejected'),
	(4,'To Interview'),
	)

POSITION_CATEGORIES = (
	('Software Engineering','Software Engineering'),
	('Product Manager','Product Manager'),
	('UI/UX Engineering','UI/UX Engineering'),
	('Marketing','Marketing'),
	('Business Development','Business Development'),
	('Growth Hacker','Growth Hacker'),
	('Accountant','Accountant'),
	('Other','Other')
	)

class Application(models.Model):
	user = models.ForeignKey(User)
	company = models.ForeignKey(Company)
	fair = models.ForeignKey(Fair)
	status = models.SmallIntegerField(choices=STATUS_CATEGORIES, default=1)
	position = models.CharField(max_length=512, default="Other")
	note = models.TextField(default='', blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	response_timestamp = models.DateTimeField(blank=True, null=True)

	def get_resume(self):
		resume = Resume.objects.filter(user=self.user, showcase=True, original=True).order_by('-timestamp')
		if len(resume) > 0:
			resume = resume[0]
			return resume.url
		else:
			resume = None
			return None

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

def auto_update_response_time(sender, instance, **kwargs):
	"""
	auto update the response_timestamp field if the status changes to 3 or 4
	- sends user email as a result

	# check if current status is 3 or 4
	# if current status is 3 or 4 - don't do anything
	# if current status is 1 or 2 and the update_field is to update it to 3 or 4
		#  then update response_timestamp
		#  send user email about update
	"""
	try:
		current_app = Application.objects.get(id=instance.id)
		if (current_app.status == 1 or current_app.status == 2) and (instance.status == 3 or instance.status == 4):
			# update response_time
			instance.response_timestamp = datetime.datetime.now()
			# send user email that he got rejected/called for interview
			template_html = 'emails/new_notification.html'
			template_text = 'emails/new_notification.txt'

			subject = "[Occuhunt] "+current_app.company.name+" Application Update"
			from_email = 'occuhunt@gmail.com'
			to_email = current_app.user.email

			text_content = render_to_string(template_text, {'name':current_app.user.first_name+' '+current_app.user.last_name, 'company':current_app.company.name, 'old_status':current_app.status, 'updated_status':instance.status})
			html_content = render_to_string(template_html, {'name':current_app.user.first_name+' '+current_app.user.last_name, 'company':current_app.company.name, 'old_status':current_app.status, 'updated_status':instance.status})

			send_html_mail(subject, text_content, html_content, from_email, [to_email])
	except Exception, e:
		print e
		

pre_save.connect(auto_update_response_time, sender=Application)