# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Note'
        db.delete_table(u'recruiterupdates_note')


    def backwards(self, orm):
        # Adding model 'Note'
        db.create_table(u'recruiterupdates_note', (
            ('note', self.gf('django.db.models.fields.TextField')()),
            ('recruiter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recruiter_note', to=orm['users.User'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='candidate_note', to=orm['users.User'])),
        ))
        db.send_create_signal(u'recruiterupdates', ['Note'])


    models = {
        
    }

    complete_apps = ['recruiterupdates']