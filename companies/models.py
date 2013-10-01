from django.db import models
import datetime

# Create your models here.
class CompanyType(models.Model):
	type = models.CharField(max_length = 256)

	def __unicode__(self):
		return self.type


ORGANIZATION_TYPES_LIST = (
	('Accounting Services', 'Accounting Services'),
	('Aerospace/Defense', 'Aerospace/Defense'),
	('Agriculture', 'Agriculture'),
	('Architecture/Planning', 'Architecture/Planning'),
	('Arts and Entertainment', 'Arts and Entertainment'),
	('Automotive/Transportation Manufacturing', 'Automotive/Transportation Manufacturing'),
	('Biotech/Pharmaceuticals','Biotech/Pharmaceuticals'),
	('Chemicals','Chemicals'),
	('Computer Hardware','Computer Hardware'),
	('Computer Software', 'Computer Software'),
	('Consumer Products', 'Consumer Products'),
	('Diversified Services', 'Diversified Services'),
	('Education/Higher Education', 'Education/Higher Education'),
	('Electronics and Misc. Tech', 'Electronics and Misc. Tech'),
	('Energy', 'Energy'),
	('Engineering', 'Engineering'),
	('Financial Services', 'Financial Services'),
	('Food, Beverage and Tobacco', 'Food, Beverage and Tobacco'),
	('Government', 'Government'),
	('Health Products and Services', 'Health Products and Services'),
	('Hospital/Healthcare', 'Hospital/Healthcare'),
	('Insurance', 'Insurance'),
	('Law/Law Related', 'Law/Law Related'),
	('Leisure and Travel', 'Leisure and Travel'),
	('Materials and Construction', 'Materials and Construction'),
	('Media', 'Media'),
	('Metals and Mining', 'Metals and Mining'),
	('Non-Profit and Social Services', 'Non-Profit and Social Services'),
	('Other Manufacturing', 'Other Manufacturing'),
	('Professional, Technical, and Administrative Services', 'Professional, Technical, and Administrative Services'),
	('Real Estate', 'Real Estate'),
	('Retail and Wholesale Trade', 'Retail and Wholesale Trade'),
	('Telecommunications', 'Telecommunications'),
	('Transportation Services', 'Transportation Services'),
	('Utilities', 'Utilities'),
	('Other', 'Other'),
	)

class Company(models.Model):
	name = models.CharField(max_length=512)
	founded = models.CharField(max_length=64, null=True, blank=True)
	funding = models.CharField(max_length=64, null=True, blank=True)
	website = models.URLField(max_length=512, null=True, blank=True)
	careers_website = models.URLField(max_length=512, null=True, blank=True)
	logo = models.URLField(max_length=512, null=True, blank=True)
	banner_image = models.URLField(max_length=512, null=True, blank=True)
	number_employees = models.CharField(max_length=48, null=True, blank=True)
	organization_type = models.TextField(null=True, blank=True, choices=ORGANIZATION_TYPES_LIST)
	company_description = models.TextField(null=True, blank=True)
	competitors = models.CharField(max_length=512, null=True, blank=True)
	avg_salary = models.CharField(max_length=64, null=True, blank=True)
	location = models.CharField(max_length=512, null=True, blank=True)
	intro_video = models.TextField(null=True, blank=True)

	def __unicode__(self):
		return self.name