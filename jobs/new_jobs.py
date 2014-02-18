#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jobs.models import Job
from companies.models import Company
from django.contrib.auth.models import Group
from fairs.models import Fair
from users.models import User

JOB_TYPES_LIST = (
	('Professional Svcs', 'Professional Svcs'),
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

new_job = Job(name='Planning', description='', job_type='Professional Svcs', company=Company.objects.get(id=657), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Marketing', description='', job_type='Marketing/PR/Product Mktg', company=Company.objects.get(id=657), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Legislative Affairs & Community Relations', description='', job_type='Professional Svcs', company=Company.objects.get(id=657), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Human Resources', description='', job_type='Professional Svcs', company=Company.objects.get(id=657), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Management', description='', job_type='Professional Svcs', company=Company.objects.get(id=657), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Activists for Social Development Fellowship', description='', job_type='Professional Svcs', company=Company.objects.get(id=644), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Donor Development Intern', description='', job_type='Professional Svcs', company=Company.objects.get(id=644), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Youth Programs Intern', description='', job_type='Professional Svcs', company=Company.objects.get(id=644), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Outreach Intern', description='', job_type='Professional Svcs', company=Company.objects.get(id=644), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Volunteer Management Intern', description='', job_type='Professional Svcs', company=Company.objects.get(id=644), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Summer Sales Intern', description='', job_type='Professional Svcs', company=Company.objects.get(id=351), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Interns in finance, risk, wealth mgmt, commercial banking & more!', description='', job_type='Professional Svcs', company=Company.objects.get(id=661), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='After School Instructor', description='', job_type='Professional Svcs', company=Company.objects.get(id=639), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='After School Program Leader', description='', job_type='Professional Svcs', company=Company.objects.get(id=639), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Community Educator', description='', job_type='Professional Svcs', company=Company.objects.get(id=639), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Career and Education Drop-In Services Mentor', description='', job_type='Professional Svcs', company=Company.objects.get(id=639), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Intake Case Manager', description='', job_type='Professional Svcs', company=Company.objects.get(id=639), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Rise Up Team Lead - Community Outreach', description='', job_type='Professional Svcs', company=Company.objects.get(id=639), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Health Educator', description='', job_type='Professional Svcs', company=Company.objects.get(id=639), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Garden Teacher', description='', job_type='Professional Svcs', company=Company.objects.get(id=639), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Residential Counselor Assistant', description='', job_type='Professional Svcs', company=Company.objects.get(id=639), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Police Aide', description='', job_type='Professional Svcs', company=Company.objects.get(id=637), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Summer Associate', description='', job_type='Professional Svcs', company=Company.objects.get(id=651), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Summer Teaching Fellow', description='', job_type='Professional Svcs', company=Company.objects.get(id=645), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Economics Major Intern', description='', job_type='Professional Svcs', company=Company.objects.get(id=650), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Computer Science Major Intern', description='', job_type='Professional Svcs', company=Company.objects.get(id=650), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='MIS Major Intern', description='', job_type='Professional Svcs', company=Company.objects.get(id=650), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Business Major Intern', description='', job_type='Professional Svcs', company=Company.objects.get(id=650), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Artistic Learning, Artistic, Development, Special Events, Marketing, Triangle Lab, Costume Design, Costume Shop, Lighting Design, Production Management, Properties, Scenic Construction, Scenic Painting, Sound Design, Stage Management, Wigs and Makeup', description='', job_type='Professional Svcs', company=Company.objects.get(id=631), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Sales Internship', description='', job_type='Sales', company=Company.objects.get(id=660), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='City Hall Fellow', description='', job_type='Professional Svcs', company=Company.objects.get(id=643), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Internship in Marketing', description='', job_type='Marketing/PR/Product Mktg', company=Company.objects.get(id=634), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Internship in Financial Services', description='', job_type='Accounting/Finance', company=Company.objects.get(id=634), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Internship in Portfolio Management', description='', job_type='Professional Svcs', company=Company.objects.get(id=634), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Internship in Institutional Services', description='', job_type='Professional Svcs', company=Company.objects.get(id=634), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Internship in Investment Analytics and Data', description='', job_type='Professional Svcs', company=Company.objects.get(id=634), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='VAS, Transfer Pricing, and Investment Banking Summer Internships (nationwide)', description='', job_type='Professional Svcs', company=Company.objects.get(id=633), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Prospective Math Teacher', description='', job_type='Professional Svcs', company=Company.objects.get(id=640), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Marketing & Sales Intern', description='', job_type='Sales', company=Company.objects.get(id=655), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Entry Level Sales/Management Trainee', description='', job_type='Sales', company=Company.objects.get(id=360), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Entry Level Sales/Management Trainee Internship', description='', job_type='Sales', company=Company.objects.get(id=360), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Social Media & Marketing Intern', description='', job_type='Professional Svcs', company=Company.objects.get(id=629), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Clubhouse Manager', description='', job_type='Professional Svcs', company=Company.objects.get(id=629), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Video Production Intern', description='', job_type='Professional Svcs', company=Company.objects.get(id=629), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Web Design Intern', description='', job_type='Professional Svcs', company=Company.objects.get(id=629), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Statistics Intern', description='', job_type='Professional Svcs', company=Company.objects.get(id=629), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Sports Journalism Intern', description='', job_type='Professional Svcs', company=Company.objects.get(id=629), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Volunteer Coordination Intern', description='', job_type='Professional Svcs', company=Company.objects.get(id=629), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Community Outreach Intern', description='', job_type='Professional Svcs', company=Company.objects.get(id=629), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Public Announcer & Scoreboard Operator', description='', job_type='Professional Svcs', company=Company.objects.get(id=629), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Office Assistant', description='', job_type='Professional Svcs', company=Company.objects.get(id=629), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Intern, Summer Emerging Leaders Program at GLIDE', description='', job_type='Professional Svcs', company=Company.objects.get(id=630), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Interns', description='', job_type='', company=Company.objects.get(id=641), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Valuation Services Summer Intern', description='', job_type='Professional Svcs', company=Company.objects.get(id=646), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Business Advisory Services Summer Intern', description='', job_type='Professional Svcs', company=Company.objects.get(id=646), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='JusticeCorps Member', description='', job_type='Professional Svcs', company=Company.objects.get(id=364), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Finance', description='', job_type='Professional Svcs', company=Company.objects.get(id=635), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='IT', description='', job_type='Professional Svcs', company=Company.objects.get(id=635), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Marketing', description='', job_type='Professional Svcs', company=Company.objects.get(id=635), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Merchandising', description='', job_type='Professional Svcs', company=Company.objects.get(id=635), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Product Development', description='', job_type='Product/Project Management', company=Company.objects.get(id=635), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Account Manager', description='', job_type='Professional Svcs', company=Company.objects.get(id=647), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Business Development', description='', job_type='Business Dev', company=Company.objects.get(id=647), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Customer Service Representative', description='', job_type='Professional Svcs', company=Company.objects.get(id=647), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Purchasing assistant', description='', job_type='Professional Svcs', company=Company.objects.get(id=647), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Software Engineer', description='', job_type='Engineering Software', company=Company.objects.get(id=286), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Hardware Engineer', description='', job_type='Engineering Hardware', company=Company.objects.get(id=286), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Quality Assurance (test) Engineer', description='', job_type='Engineering QA', company=Company.objects.get(id=286), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Product/Program/Project Managers', description='', job_type='Product/Project Management', company=Company.objects.get(id=286), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Human Resources', description='', job_type='Professional Svcs', company=Company.objects.get(id=286), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Sales', description='', job_type='Sales', company=Company.objects.get(id=286), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Financial Analysis', description='', job_type='Accounting/Financial', company=Company.objects.get(id=286), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Marketing', description='', job_type='Marketing/PR/Product Mktg', company=Company.objects.get(id=286), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Public Relations', description='', job_type='Professional Svcs', company=Company.objects.get(id=286), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='New Sector Alliance: Residency in Social Enterprise (1 year)', description='', job_type='Professional Svcs', company=Company.objects.get(id=649), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='New Sector Alliance : Summer Fellowship (11 weeks)', description='', job_type='Professional Svcs', company=Company.objects.get(id=649), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='New Sector Alliance; Senior Summer Fellowship (11 weeks)', description='', job_type='Professional Svcs', company=Company.objects.get(id=649), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Financial Representative Intern', description='', job_type='Professional Svcs', company=Company.objects.get(id=372), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Media Associate', description='', job_type='Professional Svcs', company=Company.objects.get(id=561), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Strategic Marketing Analyst', description='', job_type='Marketing/PR/Product Mktg', company=Company.objects.get(id=561), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Assistant in National Spanish Language Public Radio News Service', description='', job_type='Professional Svcs', company=Company.objects.get(id=658), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Assistant in Grantwriting and Marketing - National Spanish Language Public Radio News Service', description='', job_type='Professional Svcs', company=Company.objects.get(id=658), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Tech/Developers', description='', job_type='Engineering Software', company=Company.objects.get(id=605), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Marketing', description='', job_type='Marketing/PR/Product Mktg', company=Company.objects.get(id=605), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Legal', description='', job_type='Professional Svcs', company=Company.objects.get(id=605), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Finance', description='', job_type='Accounting/Finance', company=Company.objects.get(id=605), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Product Managers', description='', job_type='Product/Project Management', company=Company.objects.get(id=656), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Project Management', description='', job_type='Product/Project Management', company=Company.objects.get(id=656), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Property Management Rotational Internship', description='', job_type='Professional Svcs', company=Company.objects.get(id=659), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Leasing Consultant', description='', job_type='Professional Svcs', company=Company.objects.get(id=659), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Property Accountant', description='', job_type='Professional Svcs', company=Company.objects.get(id=659), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Bookkeeper', description='', job_type='Professional Svcs', company=Company.objects.get(id=659), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Assistant Property Manager', description='', job_type='Professional Svcs', company=Company.objects.get(id=659), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Assistant Store Manager Internship', description='', job_type='Professional Svcs', company=Company.objects.get(id=375), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Summer Analyst', description='', job_type='Professional Svcs', company=Company.objects.get(id=652), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Student Assistant - Compliance Section', description='', job_type='Professional Svcs', company=Company.objects.get(id=528), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Executive Internship', description='', job_type='Professional Svcs', company=Company.objects.get(id=547), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Executive Team Leader', description='', job_type='Professional Svcs', company=Company.objects.get(id=547), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Customer Support Project and Data Analyst Internship', description='', job_type='Professional Svcs', company=Company.objects.get(id=619), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Supply Chain Operations Internship', description='', job_type='Professional Svcs', company=Company.objects.get(id=619), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Product Management Intern', description='', job_type='Product/Project Management', company=Company.objects.get(id=619), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Intern - Accounting & Finance', description='', job_type='Professional Svcs', company=Company.objects.get(id=592), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Development/Membership Internship', description='', job_type='Professional Svcs', company=Company.objects.get(id=632), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Communications/Writing Internship', description='', job_type='Professional Svcs', company=Company.objects.get(id=632), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Educational Programs Internshsip', description='', job_type='Professional Svcs', company=Company.objects.get(id=632), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Intern', description='', job_type='Professional Svcs', company=Company.objects.get(id=653), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Human Resources Intern', description='', job_type='Professional Svcs', company=Company.objects.get(id=648), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Sales Administration Intern', description='', job_type='Sales', company=Company.objects.get(id=648), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Marketing Intern', description='', job_type='Marketing/PR/Product Mktg', company=Company.objects.get(id=648), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Accounting & Finance Intern', description='', job_type='Accounting/Finance', company=Company.objects.get(id=648), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Vineyard Intern', description='', job_type='Professional Svcs', company=Company.objects.get(id=648), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Operations Intern', description='', job_type='Professional Svcs', company=Company.objects.get(id=304), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Various part-time internships', description='', job_type='Professional Svcs', company=Company.objects.get(id=638), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Intern', description='', job_type='Other', company=Company.objects.get(id=385), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Marketing/Sales Internship', description='', job_type='Sales', company=Company.objects.get(id=654), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='U.S. MARINE CORPS OFFICERS', description='', job_type='Professional Svcs', company=Company.objects.get(id=384), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Student Internships in Engineering', description='', job_type='Professional Svcs', company=Company.objects.get(id=448), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Student Internships in Computer Science', description='', job_type='Professional Svcs', company=Company.objects.get(id=448), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Intern - Valuation Services', description='', job_type='Professional Svcs', company=Company.objects.get(id=388), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()
new_job = Job(name='Camp Counselor', description='', job_type='Professional Svcs', company=Company.objects.get(id=636), network=Group.objects.get(id=1), fair=Fair.objects.get(id=9))
new_job.save()

