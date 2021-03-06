# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Event'
        db.delete_table(u'fairs_event')

        # Deleting field 'Fair.event'
        db.delete_column(u'fairs_fair', 'event_id')

        # Adding field 'Fair.event_type'
        db.add_column(u'fairs_fair', 'event_type',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1, max_length=3),
                      keep_default=False)

        # Adding field 'Fair.thumbnail'
        db.add_column(u'fairs_fair', 'thumbnail',
                      self.gf('django.db.models.fields.URLField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Fair.location'
        db.add_column(u'fairs_fair', 'location',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fairs.Location'], null=True, blank=True),
                      keep_default=False)

        # Removing M2M table for field job on 'Fair'
        db.delete_table(db.shorten_name(u'fairs_fair_job'))

        # Deleting field 'ThreeFiveSeven.event'
        db.delete_column(u'fairs_threefiveseven', 'event_id')

        # Adding field 'ThreeFiveSeven.fair'
        db.add_column(u'fairs_threefiveseven', 'fair',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['fairs.Fair']),
                      keep_default=False)

        # Deleting field 'Infosession.event'
        db.delete_column(u'fairs_infosession', 'event_id')

        # Adding field 'Infosession.fair'
        db.add_column(u'fairs_infosession', 'fair',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['fairs.Fair']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'fairs_event', (
            ('resume_drop', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('thumbnail', self.gf('django.db.models.fields.URLField')(max_length=1024, null=True, blank=True)),
            ('time_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('event_type', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, max_length=3)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('time_end', self.gf('django.db.models.fields.DateTimeField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fairs.Location'], null=True, blank=True)),
        ))
        db.send_create_signal(u'fairs', ['Event'])

        # Adding field 'Fair.event'
        db.add_column(u'fairs_fair', 'event',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fairs.Event'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Fair.event_type'
        db.delete_column(u'fairs_fair', 'event_type')

        # Deleting field 'Fair.thumbnail'
        db.delete_column(u'fairs_fair', 'thumbnail')

        # Deleting field 'Fair.location'
        db.delete_column(u'fairs_fair', 'location_id')

        # Adding M2M table for field job on 'Fair'
        m2m_table_name = db.shorten_name(u'fairs_fair_job')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('fair', models.ForeignKey(orm[u'fairs.fair'], null=False)),
            ('job', models.ForeignKey(orm[u'jobs.job'], null=False))
        ))
        db.create_unique(m2m_table_name, ['fair_id', 'job_id'])


        # User chose to not deal with backwards NULL issues for 'ThreeFiveSeven.event'
        raise RuntimeError("Cannot reverse this migration. 'ThreeFiveSeven.event' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ThreeFiveSeven.event'
        db.add_column(u'fairs_threefiveseven', 'event',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fairs.Event']),
                      keep_default=False)

        # Deleting field 'ThreeFiveSeven.fair'
        db.delete_column(u'fairs_threefiveseven', 'fair_id')


        # User chose to not deal with backwards NULL issues for 'Infosession.event'
        raise RuntimeError("Cannot reverse this migration. 'Infosession.event' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Infosession.event'
        db.add_column(u'fairs_infosession', 'event',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fairs.Event']),
                      keep_default=False)

        # Deleting field 'Infosession.fair'
        db.delete_column(u'fairs_infosession', 'fair_id')


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
            'intro_video': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'number_employees': ('django.db.models.fields.CharField', [], {'max_length': '48', 'null': 'True', 'blank': 'True'}),
            'organization_type': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'fairs.fair': {
            'Meta': {'object_name': 'Fair'},
            'event_type': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fairs.Location']", 'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'organizers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'organizers'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['companies.Company']"}),
            'resume_drop': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rooms': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['fairs.Room']", 'symmetrical': 'False'}),
            'sponsors': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'sponsors'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['companies.Company']"}),
            'thumbnail': ('django.db.models.fields.URLField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'time_end': ('django.db.models.fields.DateTimeField', [], {}),
            'time_start': ('django.db.models.fields.DateTimeField', [], {}),
            'venue': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'fairs.fitting': {
            'Meta': {'object_name': 'Fitting'},
            'fn': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'x1': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'x2': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'y1': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'y2': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'fairs.infosession': {
            'Meta': {'object_name': 'Infosession'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['companies.Company']"}),
            'fair': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fairs.Fair']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'fairs.location': {
            'Meta': {'object_name': 'Location'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '5', 'blank': 'True'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '5', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'})
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
        u'fairs.threefiveseven': {
            'Meta': {'object_name': 'ThreeFiveSeven'},
            'companies': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['companies.Company']", 'symmetrical': 'False'}),
            'fair': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fairs.Fair']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['fairs']