# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Races'
        db.create_table(u'core_races', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('blazon', self.gf('imagekit.models.fields.ProcessedImageField')(default=None, max_length=100, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'core', ['Races'])

        # Adding model 'Gender'
        db.create_table(u'core_gender', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'core', ['Gender'])

        # Adding model 'Face'
        db.create_table(u'core_face', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('emotion', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('race', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Races'], null=True, blank=True)),
            ('face', self.gf('imagekit.models.fields.ProcessedImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'core', ['Face'])

        # Adding model 'Category'
        db.create_table(u'core_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('alias', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=32)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('keywords', self.gf('django.db.models.fields.TextField')(max_length=2048)),
        ))
        db.send_create_signal(u'core', ['Category'])

        # Adding model 'Stem'
        db.create_table(u'core_stem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stem', self.gf('sz.core.models.LowerCaseCharField')(unique=True, max_length=32, db_index=True)),
            ('language', self.gf('sz.core.models.LowerCaseCharField')(max_length=2, db_index=True)),
        ))
        db.send_create_signal(u'core', ['Stem'])

        # Adding unique constraint on 'Stem', fields ['stem', 'language']
        db.create_unique(u'core_stem', ['stem', 'language'])

        # Adding model 'User'
        db.create_table(u'core_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('email', self.gf('django.db.models.fields.CharField')(unique=True, max_length=72, db_index=True)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_in_engine', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_confirm', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('race', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Races'], null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Gender'], null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['User'])

        # Adding model 'RegistrationProfile'
        db.create_table(u'core_registrationprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.User'], unique=True)),
            ('activation_key', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('is_sending_email_required', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
        ))
        db.send_create_signal(u'core', ['RegistrationProfile'])

        # Adding model 'Place'
        db.create_table(u'core_place', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('position', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_in_engine', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_is_active', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('crossStreet', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('city_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('fsq_id', self.gf('django.db.models.fields.CharField')(max_length=24, null=True, blank=True)),
            ('foursquare_icon_prefix', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('foursquare_icon_suffix', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Place'])


    def backwards(self, orm):
        # Removing unique constraint on 'Stem', fields ['stem', 'language']
        db.delete_unique(u'core_stem', ['stem', 'language'])

        # Deleting model 'Races'
        db.delete_table(u'core_races')

        # Deleting model 'Gender'
        db.delete_table(u'core_gender')

        # Deleting model 'Face'
        db.delete_table(u'core_face')

        # Deleting model 'Category'
        db.delete_table(u'core_category')

        # Deleting model 'Stem'
        db.delete_table(u'core_stem')

        # Deleting model 'User'
        db.delete_table(u'core_user')

        # Deleting model 'RegistrationProfile'
        db.delete_table(u'core_registrationprofile')

        # Deleting model 'Place'
        db.delete_table(u'core_place')


    models = {
        u'core.category': {
            'Meta': {'object_name': 'Category'},
            'alias': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '32'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'max_length': '2048'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'})
        },
        u'core.face': {
            'Meta': {'object_name': 'Face'},
            'emotion': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'face': ('imagekit.models.fields.ProcessedImageField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Races']", 'null': 'True', 'blank': 'True'})
        },
        u'core.gender': {
            'Meta': {'object_name': 'Gender'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'core.place': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Place'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'city_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'crossStreet': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_is_active': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'foursquare_icon_prefix': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'foursquare_icon_suffix': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'fsq_id': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_in_engine': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'position': ('django.contrib.gis.db.models.fields.PointField', [], {})
        },
        u'core.races': {
            'Meta': {'object_name': 'Races'},
            'blazon': ('imagekit.models.fields.ProcessedImageField', [], {'default': 'None', 'max_length': '100', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'core.registrationprofile': {
            'Meta': {'object_name': 'RegistrationProfile'},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_sending_email_required': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.User']", 'unique': 'True'})
        },
        u'core.stem': {
            'Meta': {'unique_together': "(('stem', 'language'),)", 'object_name': 'Stem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('sz.core.models.LowerCaseCharField', [], {'max_length': '2', 'db_index': 'True'}),
            'stem': ('sz.core.models.LowerCaseCharField', [], {'unique': 'True', 'max_length': '32', 'db_index': 'True'})
        },
        u'core.user': {
            'Meta': {'object_name': 'User'},
            'date_confirm': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '72', 'db_index': 'True'}),
            'gender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Gender']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_in_engine': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Races']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['core']