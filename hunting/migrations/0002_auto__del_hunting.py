# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Hunting'
        db.delete_table(u'hunting_hunting')


    def backwards(self, orm):
        # Adding model 'Hunting'
        db.create_table(u'hunting_hunting', (
            ('test', self.gf('django.db.models.fields.CharField')(max_length=10)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'hunting', ['Hunting'])


    models = {
        
    }

    complete_apps = ['hunting']