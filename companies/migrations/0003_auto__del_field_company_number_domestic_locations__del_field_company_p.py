# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Company.number_domestic_locations'
        db.delete_column(u'companies_company', 'number_domestic_locations')

        # Deleting field 'Company.position_types'
        db.delete_column(u'companies_company', 'position_types')

        # Deleting field 'Company.expected_hires'
        db.delete_column(u'companies_company', 'expected_hires')

        # Deleting field 'Company.job_description'
        db.delete_column(u'companies_company', 'job_description')

        # Deleting field 'Company.number_international_locations'
        db.delete_column(u'companies_company', 'number_international_locations')

        # Deleting field 'Company.position_locations'
        db.delete_column(u'companies_company', 'position_locations')

        # Deleting field 'Company.callisto_url'
        db.delete_column(u'companies_company', 'callisto_url')

        # Adding field 'Company.founded'
        db.add_column(u'companies_company', 'founded',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Company.funding'
        db.add_column(u'companies_company', 'funding',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Company.careers_website'
        db.add_column(u'companies_company', 'careers_website',
                      self.gf('django.db.models.fields.URLField')(max_length=512, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Company.banner_image'
        db.add_column(u'companies_company', 'banner_image',
                      self.gf('django.db.models.fields.URLField')(max_length=512, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Company.competitors'
        db.add_column(u'companies_company', 'competitors',
                      self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Company.avg_salary'
        db.add_column(u'companies_company', 'avg_salary',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Company.number_domestic_locations'
        db.add_column(u'companies_company', 'number_domestic_locations',
                      self.gf('django.db.models.fields.CharField')(max_length=48, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Company.position_types'
        db.add_column(u'companies_company', 'position_types',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Company.expected_hires'
        db.add_column(u'companies_company', 'expected_hires',
                      self.gf('django.db.models.fields.CharField')(max_length=48, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Company.job_description'
        db.add_column(u'companies_company', 'job_description',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Company.number_international_locations'
        db.add_column(u'companies_company', 'number_international_locations',
                      self.gf('django.db.models.fields.CharField')(max_length=48, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Company.position_locations'
        db.add_column(u'companies_company', 'position_locations',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Company.callisto_url'
        db.add_column(u'companies_company', 'callisto_url',
                      self.gf('django.db.models.fields.URLField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Company.founded'
        db.delete_column(u'companies_company', 'founded')

        # Deleting field 'Company.funding'
        db.delete_column(u'companies_company', 'funding')

        # Deleting field 'Company.careers_website'
        db.delete_column(u'companies_company', 'careers_website')

        # Deleting field 'Company.banner_image'
        db.delete_column(u'companies_company', 'banner_image')

        # Deleting field 'Company.competitors'
        db.delete_column(u'companies_company', 'competitors')

        # Deleting field 'Company.avg_salary'
        db.delete_column(u'companies_company', 'avg_salary')


    models = {
        u'companies.company': {
            'Meta': {'object_name': 'Company'},
            'avg_salary': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'banner_image': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'careers_website': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'company_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'competitors': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'founded': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'funding': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'number_employees': ('django.db.models.fields.CharField', [], {'max_length': '48', 'null': 'True', 'blank': 'True'}),
            'organization_type': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'companies.companytype': {
            'Meta': {'object_name': 'CompanyType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['companies']