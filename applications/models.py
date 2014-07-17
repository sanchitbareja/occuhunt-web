from django.db import models
from users.models import User
from fairs.models import Fair
from companies.models import Company
from resumes.models import Resume
from jobs.models import Job
from documents.models import Document

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
	(5,'Offered'),
	(6,'Considering'),
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
	"""
	recruiter_email: email of the recruiter
	recruiter_message: email content sent by recruiter
	
	each application has multiple documents - related by ForeignKey
	"""
	user = models.ForeignKey(User)
	company = models.ForeignKey(Company)
	fair = models.ForeignKey(Fair, null=True)
	documents = models.ManyToManyField(Document, null=True)
	status = models.SmallIntegerField(choices=STATUS_CATEGORIES, default=1)
	position = models.CharField(max_length=512, default="Other")
	timestamp = models.DateTimeField(auto_now_add=True)
	response_timestamp = models.DateTimeField(blank=True, null=True)
	job = models.ForeignKey(Job, blank=True, null=True)
	student_note = models.TextField(default='', blank=True)
	note = models.TextField(default='', blank=True)
	recruiter_email = models.EmailField(max_length=200, blank=True, null=True)
	recruiter_message = models.TextField(default='', blank=True)
	added_by_user = models.BooleanField(default=False)

	def get_documents(self):
		return self.documents.all()

	def get_resume(self):
		resume = Resume.objects.filter(user=self.user, showcase=True, original=True).order_by('-timestamp')
		if len(resume) > 0:
			resume = resume[0]
			return resume.url
		else:
			resume = None
			return None

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
			recruiter_email = instance.recruiter_email
			recruiter_message = instance.recruiter_message
			to_email = current_app.user.email

			text_content = render_to_string(template_text, {'name':current_app.user.first_name+' '+current_app.user.last_name, 'company':current_app.company.name, 'old_status':current_app.status, 'updated_status':instance.status, 'recruiter_message':recruiter_message})
			html_content = render_to_string(template_html, {'name':current_app.user.first_name+' '+current_app.user.last_name, 'company':current_app.company.name, 'old_status':current_app.status, 'updated_status':instance.status, 'recruiter_message':recruiter_message})

			if recruiter_email:
				send_html_mail(subject, text_content, html_content, from_email, [to_email, recruiter_email])
			else:
				send_html_mail(subject, text_content, html_content, from_email, [to_email])
	except Exception, e:
		print e
		

pre_save.connect(auto_update_response_time, sender=Application)