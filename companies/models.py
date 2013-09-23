from django.db import models
import datetime

# Create your models here.
class CompanyType(models.Model):
	type = models.CharField(max_length = 256)

	def __unicode__(self):
		return self.type


class Company(models.Model):
	name = models.CharField(max_length=512)
	founded = models.CharField(max_length=64, null=True, blank=True)
	funding = models.CharField(max_length=64, null=True, blank=True)
	website = models.URLField(max_length=512, null=True, blank=True)
	careers_website = models.URLField(max_length=512, null=True, blank=True)
	logo = models.URLField(max_length=512, null=True, blank=True)
	banner_image = models.URLField(max_length=512, null=True, blank=True)
	number_employees = models.CharField(max_length=48, null=True, blank=True)
	organization_type = models.TextField(null=True, blank=True)
	company_description = models.TextField(null=True, blank=True)
	competitors = models.CharField(max_length=512, null=True, blank=True)
	avg_salary = models.CharField(max_length=64, null=True, blank=True)

	def __unicode__(self):
		return self.name