# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Fitting'
        db.create_table(u'fairs_fitting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('x1', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('y1', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('x2', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('y2', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('fn', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.URLField')(max_length=512, null=True, blank=True)),
        ))
        db.send_create_signal(u'fairs', ['Fitting'])

        # Adding model 'Map'
        db.create_table(u'fairs_map', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'fairs', ['Map'])

        # Adding M2M table for field tables on 'Map'
        m2m_table_name = db.shorten_name(u'fairs_map_tables')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('map', models.ForeignKey(orm[u'fairs.map'], null=False)),
            ('table', models.ForeignKey(orm[u'fairs.table'], null=False))
        ))
        db.create_unique(m2m_table_name, ['map_id', 'table_id'])

        # Adding M2M table for field fittings on 'Map'
        m2m_table_name = db.shorten_name(u'fairs_map_fittings')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('map', models.ForeignKey(orm[u'fairs.map'], null=False)),
            ('fitting', models.ForeignKey(orm[u'fairs.fitting'], null=False))
        ))
        db.create_unique(m2m_table_name, ['map_id', 'fitting_id'])

        # Adding model 'Table'
        db.create_table(u'fairs_table', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('x', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('y', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('width', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('height', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('rotation', self.gf('django.db.models.fields.PositiveIntegerField')(default=90)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['companies.Company'])),
        ))
        db.send_create_signal(u'fairs', ['Table'])

        # Adding model 'Event'
        db.create_table(u'fairs_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('time_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('time_end', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'fairs', ['Event'])

        # Adding field 'Fair.event'
        db.add_column(u'fairs_fair', 'event',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fairs.Event'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Fair.resume_drop'
        db.add_column(u'fairs_fair', 'resume_drop',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding M2M table for field organizers on 'Fair'
        m2m_table_name = db.shorten_name(u'fairs_fair_organizers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('fair', models.ForeignKey(orm[u'fairs.fair'], null=False)),
            ('company', models.ForeignKey(orm[u'companies.company'], null=False))
        ))
        db.create_unique(m2m_table_name, ['fair_id', 'company_id'])

        # Adding M2M table for field sponsors on 'Fair'
        m2m_table_name = db.shorten_name(u'fairs_fair_sponsors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('fair', models.ForeignKey(orm[u'fairs.fair'], null=False)),
            ('company', models.ForeignKey(orm[u'companies.company'], null=False))
        ))
        db.create_unique(m2m_table_name, ['fair_id', 'company_id'])

        # Adding M2M table for field job on 'Fair'
        m2m_table_name = db.shorten_name(u'fairs_fair_job')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('fair', models.ForeignKey(orm[u'fairs.fair'], null=False)),
            ('job', models.ForeignKey(orm[u'jobs.job'], null=False))
        ))
        db.create_unique(m2m_table_name, ['fair_id', 'job_id'])

        # Adding field 'Room.lat'
        db.add_column(u'fairs_room', 'lat',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=5, blank=True),
                      keep_default=False)

        # Adding field 'Room.lng'
        db.add_column(u'fairs_room', 'lng',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=5, blank=True),
                      keep_default=False)

        # Adding field 'Room.map'
        db.add_column(u'fairs_room', 'map',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fairs.Map'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Fitting'
        db.delete_table(u'fairs_fitting')

        # Deleting model 'Map'
        db.delete_table(u'fairs_map')

        # Removing M2M table for field tables on 'Map'
        db.delete_table(db.shorten_name(u'fairs_map_tables'))

        # Removing M2M table for field fittings on 'Map'
        db.delete_table(db.shorten_name(u'fairs_map_fittings'))

        # Deleting model 'Table'
        db.delete_table(u'fairs_table')

        # Deleting model 'Event'
        db.delete_table(u'fairs_event')

        # Deleting field 'Fair.event'
        db.delete_column(u'fairs_fair', 'event_id')

        # Deleting field 'Fair.resume_drop'
        db.delete_column(u'fairs_fair', 'resume_drop')

        # Removing M2M table for field organizers on 'Fair'
        db.delete_table(db.shorten_name(u'fairs_fair_organizers'))

        # Removing M2M table for field sponsors on 'Fair'
        db.delete_table(db.shorten_name(u'fairs_fair_sponsors'))

        # Removing M2M table for field job on 'Fair'
        db.delete_table(db.shorten_name(u'fairs_fair_job'))

        # Deleting field 'Room.lat'
        db.delete_column(u'fairs_room', 'lat')

        # Deleting field 'Room.lng'
        db.delete_column(u'fairs_room', 'lng')

        # Deleting field 'Room.map'
        db.delete_column(u'fairs_room', 'map_id')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
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
            'intro_video': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'number_employees': ('django.db.models.fields.CharField', [], {'max_length': '48', 'null': 'True', 'blank': 'True'}),
            'organization_type': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'fairs.event': {
            'Meta': {'object_name': 'Event'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'time_end': ('django.db.models.fields.DateTimeField', [], {}),
            'time_start': ('django.db.models.fields.DateTimeField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'fairs.fair': {
            'Meta': {'object_name': 'Fair'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fairs.Event']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['jobs.Job']", 'symmetrical': 'False'}),
            'logo': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'organizers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'organizers'", 'symmetrical': 'False', 'to': u"orm['companies.Company']"}),
            'resume_drop': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rooms': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['fairs.Room']", 'symmetrical': 'False'}),
            'sponsors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'sponsors'", 'symmetrical': 'False', 'to': u"orm['companies.Company']"}),
            'time_end': ('django.db.models.fields.DateTimeField', [], {}),
            'time_start': ('django.db.models.fields.DateTimeField', [], {}),
            'venue': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'fairs.fitting': {
            'Meta': {'object_name': 'Fitting'},
            'fn': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'x1': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'x2': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'y1': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'y2': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'fairs.map': {
            'Meta': {'object_name': 'Map'},
            'fittings': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['fairs.Fitting']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tables': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['fairs.Table']", 'symmetrical': 'False'})
        },
        u'fairs.room': {
            'Meta': {'object_name': 'Room'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '5', 'blank': 'True'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '5', 'blank': 'True'}),
            'map': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fairs.Map']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'fairs.table': {
            'Meta': {'object_name': 'Table'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['companies.Company']"}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rotation': ('django.db.models.fields.PositiveIntegerField', [], {'default': '90'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'x': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'y': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'jobs.job': {
            'Meta': {'object_name': 'Job'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['companies.Company']"}),
            'contract_type': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'deactivate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_type': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']", 'null': 'True', 'blank': 'True'}),
            'qualifications': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['fairs']