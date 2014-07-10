# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Hunt'
        db.delete_table(u'hunts_hunt')


    def backwards(self, orm):
        # Adding model 'Hunt'
        db.create_table(u'hunts_hunt', (
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fair', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fairs.Fair'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
        ))
        db.send_create_signal(u'hunts', ['Hunt'])


    models = {
        
    }

    complete_apps = ['hunts']