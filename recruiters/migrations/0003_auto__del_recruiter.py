# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Recruiter'
        db.delete_table(u'recruiters_recruiter')


    def backwards(self, orm):
        # Adding model 'Recruiter'
        db.create_table(u'recruiters_recruiter', (
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['companies.Company'])),
            (u'user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['users.User'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'recruiters', ['Recruiter'])


    models = {
        
    }

    complete_apps = ['recruiters']