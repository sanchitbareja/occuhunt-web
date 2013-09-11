# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Fair'
        db.create_table(u'fairs_fair', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('venue', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('date_start', self.gf('django.db.models.fields.DateField')(default=0)),
            ('date_end', self.gf('django.db.models.fields.DateField')(default=0)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal(u'fairs', ['Fair'])


    def backwards(self, orm):
        # Deleting model 'Fair'
        db.delete_table(u'fairs_fair')


    models = {
        u'fairs.fair': {
            'Meta': {'object_name': 'Fair'},
            'date_end': ('django.db.models.fields.DateField', [], {'default': '0'}),
            'date_start': ('django.db.models.fields.DateField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'venue': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['fairs']