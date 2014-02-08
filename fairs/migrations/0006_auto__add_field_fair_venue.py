# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Fair.venue'
        db.add_column(u'fairs_fair', 'venue',
                      self.gf('django.db.models.fields.CharField')(default='International House', max_length=512),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Fair.venue'
        db.delete_column(u'fairs_fair', 'venue')


    models = {
        u'fairs.fair': {
            'Meta': {'object_name': 'Fair'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'rooms': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['fairs.Room']", 'symmetrical': 'False'}),
            'time_end': ('django.db.models.fields.DateTimeField', [], {}),
            'time_start': ('django.db.models.fields.DateTimeField', [], {}),
            'venue': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'fairs.room': {
            'Meta': {'object_name': 'Room'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['fairs']