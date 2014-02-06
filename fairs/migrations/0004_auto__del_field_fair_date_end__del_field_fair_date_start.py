# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Fair.date_end'
        db.delete_column(u'fairs_fair', 'date_end')

        # Deleting field 'Fair.date_start'
        db.delete_column(u'fairs_fair', 'date_start')


    def backwards(self, orm):
        # Adding field 'Fair.date_end'
        db.add_column(u'fairs_fair', 'date_end',
                      self.gf('django.db.models.fields.DateField')(default=0),
                      keep_default=False)

        # Adding field 'Fair.date_start'
        db.add_column(u'fairs_fair', 'date_start',
                      self.gf('django.db.models.fields.DateField')(default=0),
                      keep_default=False)


    models = {
        u'fairs.fair': {
            'Meta': {'object_name': 'Fair'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'rooms': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['fairs.Room']", 'symmetrical': 'False'})
        },
        u'fairs.room': {
            'Meta': {'object_name': 'Room'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['fairs']