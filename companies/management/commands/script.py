# coding: utf-8

from django.core.management.base import BaseCommand, CommandError
from companies.models import Company
import csv
import os

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        data = csv.reader(open(os.getcwd()+'/companies/management/commands/CCFInfo3.csv', 'rU'), quotechar='"', delimiter = ',') 
        # print (data)
        for row in data:
            # print "0"+row[0]
            new_company = Company(name=row[0], callisto_url=row[1], website=row[2], logo=row[3], expected_hires=row[4], number_employees=row[5], 
                number_domestic_locations=row[6], number_international_locations=row[7], organization_type=row[8], company_description=row[9],
            job_description=row[10], position_locations=row[11], position_types=row[12])
            new_company.save()
        self.stdout.write('Success')
