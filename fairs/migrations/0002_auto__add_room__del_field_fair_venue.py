# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Room'
        db.create_table(u'fairs_room', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal(u'fairs', ['Room'])

        # Deleting field 'Fair.venue'
        db.delete_column(u'fairs_fair', 'venue')

        # Adding M2M table for field rooms on 'Fair'
        m2m_table_name = db.shorten_name(u'fairs_fair_rooms')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('fair', models.ForeignKey(orm[u'fairs.fair'], null=False)),
            ('room', models.ForeignKey(orm[u'fairs.room'], null=False))
        ))
        db.create_unique(m2m_table_name, ['fair_id', 'room_id'])


    def backwards(self, orm):
        # Deleting model 'Room'
        db.delete_table(u'fairs_room')

        # Adding field 'Fair.venue'
        db.add_column(u'fairs_fair', 'venue',
                      self.gf('django.db.models.fields.CharField')(default='UC Berkeley', max_length=512),
                      keep_default=False)

        # Removing M2M table for field rooms on 'Fair'
        db.delete_table(db.shorten_name(u'fairs_fair_rooms'))


    models = {
        u'fairs.fair': {
            'Meta': {'object_name': 'Fair'},
            'date_end': ('django.db.models.fields.DateField', [], {'default': '0'}),
            'date_start': ('django.db.models.fields.DateField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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