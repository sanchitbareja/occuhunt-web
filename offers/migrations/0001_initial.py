# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Offer'
        db.create_table(u'offers_offer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('company_from_text', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('company_from', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['companies.Company'], null=True, blank=True)),
            ('company_category', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('number_of_offers', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('salary_range', self.gf('django.db.models.fields.SmallIntegerField')(default=15)),
            ('offer_deadline', self.gf('django.db.models.fields.SmallIntegerField')(default=3)),
            ('interested_in_startups', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('interested_in_corps', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('companies_considering', self.gf('django.db.models.fields.TextField')()),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'offers', ['Offer'])


    def backwards(self, orm):
        # Deleting model 'Offer'
        db.delete_table(u'offers_offer')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'companies.company': {
            'Meta': {'object_name': 'Company'},
            'avg_salary': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'banner_image': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'careers_website': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'company_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'competitors': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'founded': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'funding': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro_video': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'number_employees': ('django.db.models.fields.CharField', [], {'max_length': '48', 'null': 'True', 'blank': 'True'}),
            'organization_type': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'offers.offer': {
            'Meta': {'object_name': 'Offer'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'companies_considering': ('django.db.models.fields.TextField', [], {}),
            'company_category': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'company_from': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['companies.Company']", 'null': 'True', 'blank': 'True'}),
            'company_from_text': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interested_in_corps': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'interested_in_startups': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number_of_offers': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'offer_deadline': ('django.db.models.fields.SmallIntegerField', [], {'default': '3'}),
            'salary_range': ('django.db.models.fields.SmallIntegerField', [], {'default': '15'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"})
        },
        u'users.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'linkedin_uid': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'profile_pic': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'resume_points': ('django.db.models.fields.IntegerField', [], {'default': "'0'"}),
            'thumbnail_profile_pic': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'verification_token': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['offers']