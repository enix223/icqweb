# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Package'
        db.create_table(u'app_package', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('package_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('flow_limit', self.gf('django.db.models.fields.BigIntegerField')()),
            ('time_limit', self.gf('django.db.models.fields.IntegerField')()),
            ('time_unit', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('package_ad_img', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('package_price', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('package_desc', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'app', ['Package'])

        # Adding model 'UserPackageRel'
        db.create_table(u'app_userpackagerel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('package', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['app.Package'], unique=True)),
            ('register_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('upload', self.gf('django.db.models.fields.IntegerField')()),
            ('download', self.gf('django.db.models.fields.IntegerField')()),
            ('expired_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'app', ['UserPackageRel'])

        # Adding model 'UserProfile'
        db.create_table(u'app_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('passwd', self.gf('django.db.models.fields.CharField')(default=u'msFtJuDRlW', max_length=10)),
        ))
        db.send_create_signal(u'app', ['UserProfile'])


    def backwards(self, orm):
        # Deleting model 'Package'
        db.delete_table(u'app_package')

        # Deleting model 'UserPackageRel'
        db.delete_table(u'app_userpackagerel')

        # Deleting model 'UserProfile'
        db.delete_table(u'app_userprofile')


    models = {
        u'app.package': {
            'Meta': {'object_name': 'Package'},
            'flow_limit': ('django.db.models.fields.BigIntegerField', [], {}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_ad_img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'package_desc': ('django.db.models.fields.TextField', [], {}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'package_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'time_limit': ('django.db.models.fields.IntegerField', [], {}),
            'time_unit': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'app.userpackagerel': {
            'Meta': {'object_name': 'UserPackageRel'},
            'download': ('django.db.models.fields.IntegerField', [], {}),
            'expired_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['app.Package']", 'unique': 'True'}),
            'register_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'upload': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'app.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'passwd': ('django.db.models.fields.CharField', [], {'default': "u'msFtJuDRlW'", 'max_length': '10'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['app']