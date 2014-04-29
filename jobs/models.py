from django.db import models
from companies.models import Company
from django.contrib.auth.models import Group
from users.models import User

import datetime

# Create your models here.
JOB_TYPES_LIST = (
	('Engineering Software', 'Engineering Software'),
	('Engineering Hardware', 'Engineering Hardware'),
	('Product/Project Management', 'Product/Project Management'),
	('Engineering QA', 'Engineering QA'),
	('WebDev/Design/Internet', 'WebDev/Design/Internet'),
	('Tech Ops/Data', 'Tech Ops/Data'),
	('Technical/Customer Support', 'Technical/Customer Support'),
	('Manufacturing', 'Manufacturing'),
	('Life Sciences', 'Life Sciences'),
	('Marketing/PR/Product Mktg', 'Marketing/PR/Product Mktg'),
	('Sales','Sales'),
	('Business Dev', 'Business Dev'),
	('Professional Svcs', 'Professional Svcs'),
	('Accounting/Finance', 'Accounting/Finance'),
	('HR/Recruiting','HR/Recruiting'),
	('Administration', 'Administration'),
	('Legal', 'Legal'),
	('Operations', 'Operations'),
	('Other','Other'),
	)

JOB_CONTRACT_TYPES = (
	(1, 'Internship'),
	(2, 'Full Time'),
	(3, 'Part Time'),
	)

class Job(models.Model):
	name = models.CharField(max_length=512)
	description = models.TextField(null=True, blank=True)
	job_type = models.CharField(max_length=512, null=True, blank=True, choices=JOB_TYPES_LIST)
	location = models.CharField(max_length=512, null=True, blank=True)
	company = models.ForeignKey(Company)
	network = models.ForeignKey(Group, null=True, blank=True)
	deactivate = models.BooleanField(default=False)
	contract_type = models.SmallIntegerField(null=True, blank=True, choices=JOB_CONTRACT_TYPES)
	qualifications = models.TextField(blank=True, null=True)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __unicode__(self):
		return self.name