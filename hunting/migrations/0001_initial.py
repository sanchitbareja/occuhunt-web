# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Hunting'
        db.create_table(u'hunting_hunting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('test', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'hunting', ['Hunting'])


    def backwards(self, orm):
        # Deleting model 'Hunting'
        db.delete_table(u'hunting_hunting')


    models = {
        u'hunting.hunting': {
            'Meta': {'object_name': 'Hunting'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'test': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['hunting']