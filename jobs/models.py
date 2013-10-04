from django.db import models
from companies.models import Company
from fairs.models import Fair
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
	)


class Job(models.Model):
	name = models.CharField(max_length=512)
	job_type = models.CharField(max_length=512, null=True, blank=True, choices=JOB_TYPES_LIST)
	location = models.CharField(max_length=512, null=True, blank=True)
	company = models.ForeignKey(Company)
	fair = models.ForeignKey(Fair, null=True, blank=True)

	def __unicode__(self):
		return self.name