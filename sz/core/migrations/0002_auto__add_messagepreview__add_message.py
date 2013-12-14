# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MessagePreview'
        db.create_table(u'core_messagepreview', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=1024, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.User'])),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Place'])),
            ('photo', self.gf('imagekit.models.fields.ProcessedImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'core', ['MessagePreview'])

        # Adding M2M table for field categories on 'MessagePreview'
        m2m_table_name = db.shorten_name(u'core_messagepreview_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('messagepreview', models.ForeignKey(orm[u'core.messagepreview'], null=False)),
            ('category', models.ForeignKey(orm[u'core.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['messagepreview_id', 'category_id'])

        # Adding model 'Message'
        db.create_table(u'core_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=1024, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.User'])),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Place'])),
            ('photo', self.gf('imagekit.models.fields.ProcessedImageField')(max_length=100, blank=True)),
            ('face', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Face'], null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Message'])

        # Adding M2M table for field categories on 'Message'
        m2m_table_name = db.shorten_name(u'core_message_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('message', models.ForeignKey(orm[u'core.message'], null=False)),
            ('category', models.ForeignKey(orm[u'core.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['message_id', 'category_id'])

        # Adding M2M table for field stems on 'Message'
        m2m_table_name = db.shorten_name(u'core_message_stems')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('message', models.ForeignKey(orm[u'core.message'], null=False)),
            ('stem', models.ForeignKey(orm[u'core.stem'], null=False))
        ))
        db.create_unique(m2m_table_name, ['message_id', 'stem_id'])


    def backwards(self, orm):
        # Deleting model 'MessagePreview'
        db.delete_table(u'core_messagepreview')

        # Removing M2M table for field categories on 'MessagePreview'
        db.delete_table(db.shorten_name(u'core_messagepreview_categories'))

        # Deleting model 'Message'
        db.delete_table(u'core_message')

        # Removing M2M table for field categories on 'Message'
        db.delete_table(db.shorten_name(u'core_message_categories'))

        # Removing M2M table for field stems on 'Message'
        db.delete_table(db.shorten_name(u'core_message_stems'))


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
        u'core.message': {
            'Meta': {'object_name': 'Message'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.Category']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'face': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Face']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('imagekit.models.fields.ProcessedImageField', [], {'max_length': '100', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Place']"}),
            'stems': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.Stem']", 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.User']"})
        },
        u'core.messagepreview': {
            'Meta': {'object_name': 'MessagePreview'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.Category']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('imagekit.models.fields.ProcessedImageField', [], {'max_length': '100', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Place']"}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.User']"})
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