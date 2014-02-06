# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Fair.time_start'
        db.add_column(u'fairs_fair', 'time_start',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 2, 6, 0, 0)),
                      keep_default=False)

        # Adding field 'Fair.time_end'
        db.add_column(u'fairs_fair', 'time_end',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 2, 6, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Fair.time_start'
        db.delete_column(u'fairs_fair', 'time_start')

        # Deleting field 'Fair.time_end'
        db.delete_column(u'fairs_fair', 'time_end')


    models = {
        u'fairs.fair': {
            'Meta': {'object_name': 'Fair'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'rooms': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['fairs.Room']", 'symmetrical': 'False'}),
            'time_end': ('django.db.models.fields.DateTimeField', [], {}),
            'time_start': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'fairs.room': {
            'Meta': {'object_name': 'Room'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['fairs']