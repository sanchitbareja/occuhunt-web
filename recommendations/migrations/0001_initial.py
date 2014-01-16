# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Request'
        db.create_table(u'recommendations_request', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('request_from', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('request_to', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('relationship', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('project', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('deadline', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'recommendations', ['Request'])


    def backwards(self, orm):
        # Deleting model 'Request'
        db.delete_table(u'recommendations_request')


    models = {
        u'recommendations.request': {
            'Meta': {'object_name': 'Request'},
            'deadline': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'request_from': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'request_to': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['recommendations']