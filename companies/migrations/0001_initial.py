# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CompanyType'
        db.create_table(u'companies_companytype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'companies', ['CompanyType'])

        # Adding model 'Company'
        db.create_table(u'companies_company', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('callisto_url', self.gf('django.db.models.fields.URLField')(max_length=1024)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=512)),
            ('logo', self.gf('django.db.models.fields.URLField')(max_length=512)),
            ('expected_hires', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('number_employees', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('number_domestic_locations', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('number_international_locations', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('company_description', self.gf('django.db.models.fields.TextField')()),
            ('job_description', self.gf('django.db.models.fields.TextField')()),
            ('position_locations', self.gf('django.db.models.fields.TextField')()),
            ('position_types', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'companies', ['Company'])

        # Adding M2M table for field organization_type on 'Company'
        m2m_table_name = db.shorten_name(u'companies_company_organization_type')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('company', models.ForeignKey(orm[u'companies.company'], null=False)),
            ('companytype', models.ForeignKey(orm[u'companies.companytype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['company_id', 'companytype_id'])


    def backwards(self, orm):
        # Deleting model 'CompanyType'
        db.delete_table(u'companies_companytype')

        # Deleting model 'Company'
        db.delete_table(u'companies_company')

        # Removing M2M table for field organization_type on 'Company'
        db.delete_table(db.shorten_name(u'companies_company_organization_type'))


    models = {
        u'companies.company': {
            'Meta': {'object_name': 'Company'},
            'callisto_url': ('django.db.models.fields.URLField', [], {'max_length': '1024'}),
            'company_description': ('django.db.models.fields.TextField', [], {}),
            'expected_hires': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_description': ('django.db.models.fields.TextField', [], {}),
            'logo': ('django.db.models.fields.URLField', [], {'max_length': '512'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'number_domestic_locations': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'number_employees': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'number_international_locations': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'organization_type': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['companies.CompanyType']", 'null': 'True', 'blank': 'True'}),
            'position_locations': ('django.db.models.fields.TextField', [], {}),
            'position_types': ('django.db.models.fields.TextField', [], {}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '512'})
        },
        u'companies.companytype': {
            'Meta': {'object_name': 'CompanyType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['companies']