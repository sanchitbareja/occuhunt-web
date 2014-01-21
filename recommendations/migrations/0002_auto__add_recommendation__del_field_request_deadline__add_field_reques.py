# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Recommendation'
        db.create_table(u'recommendations_recommendation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recommendation_from', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('recommendation_to', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('relationship', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('project', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('answer1', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('answer2', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('answer3', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'recommendations', ['Recommendation'])

        # Deleting field 'Request.deadline'
        db.delete_column(u'recommendations_request', 'deadline')

        # Adding field 'Request.timestamp'
        db.add_column(u'recommendations_request', 'timestamp',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Recommendation'
        db.delete_table(u'recommendations_recommendation')

        # Adding field 'Request.deadline'
        db.add_column(u'recommendations_request', 'deadline',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Request.timestamp'
        db.delete_column(u'recommendations_request', 'timestamp')


    models = {
        u'recommendations.recommendation': {
            'Meta': {'object_name': 'Recommendation'},
            'answer1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'answer2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'answer3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'recommendation_from': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'recommendation_to': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'recommendations.request': {
            'Meta': {'object_name': 'Request'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'request_from': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'request_to': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['recommendations']