from django.db import models
import datetime

# Create your models here.
class CompanyType(models.Model):
	type = models.CharField(max_length = 256)

	def __unicode__(self):
		return self.type


class Company(models.Model):
	name = models.CharField(max_length=512)
	callisto_url = models.URLField(max_length=1024, null=True, blank=True)
	website = models.URLField(max_length=512, null=True, blank=True)
	logo = models.URLField(max_length=512, null=True, blank=True)
	expected_hires = models.CharField(max_length=48, null=True, blank=True)
	number_employees = models.CharField(max_length=48, null=True, blank=True)
	number_domestic_locations = models.CharField(max_length=48, null=True, blank=True)
	number_international_locations = models.CharField(max_length=48, null=True, blank=True)
	organization_type = models.TextField(null=True, blank=True)
	company_description = models.TextField(null=True, blank=True)
	job_description = models.TextField(null=True, blank=True)
	position_locations = models.TextField(null=True, blank=True)
	position_types = models.TextField(null=True, blank=True)

	def __unicode__(self):
		return self.name