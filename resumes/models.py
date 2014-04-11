from django.db import models
from django.contrib.auth.models import Group
from users.models import User
import datetime

# signals
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# misc
import datetime
from mailer import send_mail, send_html_mail
from occuhunt.settings import EMAIL_MASTERS
from django.template.loader import render_to_string

# Create your models here.
class Resume(models.Model):
	user = models.ForeignKey(User)
	url = models.URLField(max_length=1000)
	timestamp = models.DateTimeField(auto_now_add = True)
	anonymous = models.BooleanField()
	original = models.BooleanField()
	featured = models.BooleanField(default=False)
	showcase = models.BooleanField(default=False)

	def __unicode__(self):
		return str(self.user)+":"+self.url

class Comment(models.Model):
	comment = models.TextField(null = True, blank = True)
	x = models.FloatField(null = True, blank = True)
	y = models.FloatField(null = True, blank = True)
	resume = models.ForeignKey(Resume)
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.comment


# After someone posts a comment, it should send an email to the person that his resume just got commented
def inform_user_of_comment(sender, instance, **kwargs):
	"""
	When a resume receives a comment, it should send the user who owns the resume an email about the comment
	- include comment
	- include link to resume 
	Tell him that he can use the link and share around with his friends to receive feedback from family and friends

	# Get comment
	# Get email of user who owns the resume
	# Construct email
	# Send email to resume
	"""
	try:
		# get comment
		current_comment = Comment.objects.get(id=instance.id)
		# get resume
		current_resume = instance.resume
		resume_feedback_url = 'http://occuhunt.com/plan/resume-feed/'+current_resume.url[36:]
		# get email
		resume_owner = resume.user

		# contruct email
		template_html = 'email/new_comment.html'
		template_text = 'email/new_comment.txt'

		subject = "[Occuhunt] Feedback on resume: "+comment.comment+""
		from_email = 'occuhunt@gmail.com'
		to_email = resume_owner.email

		text_content = render_to_string(template_text, {'name':resume_owner.user.first_name+' '+resume_owner.user.last_name, 'comment':current_comment.comment ,'resume_feedback_url':resume_feedback_url})
		html_content = render_to_string(template_html, {'name':resume_owner.user.first_name+' '+resume_owner.user.last_name, 'comment':current_comment.comment ,'resume_feedback_url':resume_feedback_url})

		# send email
		send_html_mail(subject, text_content, html_content, from_email, [to_email])
	except Exception, e:
		print e

pre_save.connect(inform_user_of_comment, sender=Comment)
