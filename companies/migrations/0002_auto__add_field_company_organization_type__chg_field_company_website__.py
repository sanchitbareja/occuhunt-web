# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Company.organization_type'
        db.add_column(u'companies_company', 'organization_type',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Removing M2M table for field organization_type on 'Company'
        db.delete_table(db.shorten_name(u'companies_company_organization_type'))


        # Changing field 'Company.website'
        db.alter_column(u'companies_company', 'website', self.gf('django.db.models.fields.URLField')(max_length=512, null=True))

        # Changing field 'Company.number_international_locations'
        db.alter_column(u'companies_company', 'number_international_locations', self.gf('django.db.models.fields.CharField')(max_length=48, null=True))

        # Changing field 'Company.position_locations'
        db.alter_column(u'companies_company', 'position_locations', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Company.company_description'
        db.alter_column(u'companies_company', 'company_description', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Company.number_domestic_locations'
        db.alter_column(u'companies_company', 'number_domestic_locations', self.gf('django.db.models.fields.CharField')(max_length=48, null=True))

        # Changing field 'Company.callisto_url'
        db.alter_column(u'companies_company', 'callisto_url', self.gf('django.db.models.fields.URLField')(max_length=1024, null=True))

        # Changing field 'Company.position_types'
        db.alter_column(u'companies_company', 'position_types', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Company.expected_hires'
        db.alter_column(u'companies_company', 'expected_hires', self.gf('django.db.models.fields.CharField')(max_length=48, null=True))

        # Changing field 'Company.job_description'
        db.alter_column(u'companies_company', 'job_description', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Company.number_employees'
        db.alter_column(u'companies_company', 'number_employees', self.gf('django.db.models.fields.CharField')(max_length=48, null=True))

        # Changing field 'Company.logo'
        db.alter_column(u'companies_company', 'logo', self.gf('django.db.models.fields.URLField')(max_length=512, null=True))

    def backwards(self, orm):
        # Deleting field 'Company.organization_type'
        db.delete_column(u'companies_company', 'organization_type')

        # Adding M2M table for field organization_type on 'Company'
        m2m_table_name = db.shorten_name(u'companies_company_organization_type')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('company', models.ForeignKey(orm[u'companies.company'], null=False)),
            ('companytype', models.ForeignKey(orm[u'companies.companytype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['company_id', 'companytype_id'])


        # Changing field 'Company.website'
        db.alter_column(u'companies_company', 'website', self.gf('django.db.models.fields.URLField')(default='', max_length=512))

        # Changing field 'Company.number_international_locations'
        db.alter_column(u'companies_company', 'number_international_locations', self.gf('django.db.models.fields.CharField')(default='', max_length=48))

        # Changing field 'Company.position_locations'
        db.alter_column(u'companies_company', 'position_locations', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Company.company_description'
        db.alter_column(u'companies_company', 'company_description', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Company.number_domestic_locations'
        db.alter_column(u'companies_company', 'number_domestic_locations', self.gf('django.db.models.fields.CharField')(default='', max_length=48))

        # Changing field 'Company.callisto_url'
        db.alter_column(u'companies_company', 'callisto_url', self.gf('django.db.models.fields.URLField')(default='', max_length=1024))

        # Changing field 'Company.position_types'
        db.alter_column(u'companies_company', 'position_types', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Company.expected_hires'
        db.alter_column(u'companies_company', 'expected_hires', self.gf('django.db.models.fields.CharField')(default='', max_length=48))

        # Changing field 'Company.job_description'
        db.alter_column(u'companies_company', 'job_description', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Company.number_employees'
        db.alter_column(u'companies_company', 'number_employees', self.gf('django.db.models.fields.CharField')(default='', max_length=48))

        # Changing field 'Company.logo'
        db.alter_column(u'companies_company', 'logo', self.gf('django.db.models.fields.URLField')(default='', max_length=512))

    models = {
        u'companies.company': {
            'Meta': {'object_name': 'Company'},
            'callisto_url': ('django.db.models.fields.URLField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'company_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'expected_hires': ('django.db.models.fields.CharField', [], {'max_length': '48', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'number_domestic_locations': ('django.db.models.fields.CharField', [], {'max_length': '48', 'null': 'True', 'blank': 'True'}),
            'number_employees': ('django.db.models.fields.CharField', [], {'max_length': '48', 'null': 'True', 'blank': 'True'}),
            'number_international_locations': ('django.db.models.fields.CharField', [], {'max_length': '48', 'null': 'True', 'blank': 'True'}),
            'organization_type': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'position_locations': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'position_types': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'companies.companytype': {
            'Meta': {'object_name': 'CompanyType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['companies']