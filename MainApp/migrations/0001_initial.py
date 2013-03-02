# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Bar'
        db.create_table('MainApp_bar', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('icon', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('lattitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('zipcode', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('MainApp', ['Bar'])

        # Adding model 'AppUser'
        db.create_table('MainApp_appuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('birthdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('facebook_user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['MainApp.FacebookAppUser'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('MainApp', ['AppUser'])

        # Adding model 'FacebookAppUser'
        db.create_table('MainApp_facebookappuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('fb_uid', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('fb_email', self.gf('django.db.models.fields.EmailField')(max_length=255, null=True, blank=True)),
            ('oauth_token', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['MainApp.OAuthToken'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('MainApp', ['FacebookAppUser'])

        # Adding model 'OAuthToken'
        db.create_table('MainApp_oauthtoken', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('token', self.gf('django.db.models.fields.TextField')()),
            ('issued_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('expires_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('MainApp', ['OAuthToken'])

        # Adding model 'DrinkType'
        db.create_table('MainApp_drinktype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('bar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['MainApp.Bar'])),
            ('type_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('MainApp', ['DrinkType'])

        # Adding model 'Drink'
        db.create_table('MainApp_drink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('bar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['MainApp.Bar'])),
            ('drink_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['MainApp.DrinkType'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
        ))
        db.send_create_signal('MainApp', ['Drink'])

        # Adding model 'Order'
        db.create_table('MainApp_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('bar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['MainApp.Bar'])),
            ('appuser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['MainApp.AppUser'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('total', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('tax', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('sub_total', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('tip', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('grand_total', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('MainApp', ['Order'])

        # Adding model 'DrinkOrdered'
        db.create_table('MainApp_drinkordered', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['MainApp.Order'])),
            ('drink_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('unit_price', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('drink_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('MainApp', ['DrinkOrdered'])


    def backwards(self, orm):
        # Deleting model 'Bar'
        db.delete_table('MainApp_bar')

        # Deleting model 'AppUser'
        db.delete_table('MainApp_appuser')

        # Deleting model 'FacebookAppUser'
        db.delete_table('MainApp_facebookappuser')

        # Deleting model 'OAuthToken'
        db.delete_table('MainApp_oauthtoken')

        # Deleting model 'DrinkType'
        db.delete_table('MainApp_drinktype')

        # Deleting model 'Drink'
        db.delete_table('MainApp_drink')

        # Deleting model 'Order'
        db.delete_table('MainApp_order')

        # Deleting model 'DrinkOrdered'
        db.delete_table('MainApp_drinkordered')


    models = {
        'MainApp.appuser': {
            'Meta': {'ordering': "['email']", 'object_name': 'AppUser'},
            'birthdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'facebook_user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['MainApp.FacebookAppUser']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'MainApp.bar': {
            'Meta': {'ordering': "['name']", 'object_name': 'Bar'},
            'created': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'icon': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lattitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'zipcode': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'MainApp.drink': {
            'Meta': {'ordering': "['name']", 'object_name': 'Drink'},
            'bar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['MainApp.Bar']"}),
            'created': ('django.db.models.fields.DateField', [], {}),
            'drink_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['MainApp.DrinkType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'MainApp.drinkordered': {
            'Meta': {'object_name': 'DrinkOrdered'},
            'drink_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'drink_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['MainApp.Order']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'unit_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'})
        },
        'MainApp.drinktype': {
            'Meta': {'ordering': "['type_name']", 'object_name': 'DrinkType'},
            'bar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['MainApp.Bar']"}),
            'created': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'MainApp.facebookappuser': {
            'Meta': {'object_name': 'FacebookAppUser'},
            'created': ('django.db.models.fields.DateField', [], {}),
            'fb_email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fb_uid': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oauth_token': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['MainApp.OAuthToken']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'MainApp.oauthtoken': {
            'Meta': {'object_name': 'OAuthToken'},
            'expires_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issued_at': ('django.db.models.fields.DateTimeField', [], {}),
            'token': ('django.db.models.fields.TextField', [], {})
        },
        'MainApp.order': {
            'Meta': {'ordering': "['datetime']", 'object_name': 'Order'},
            'appuser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['MainApp.AppUser']"}),
            'bar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['MainApp.Bar']"}),
            'created': ('django.db.models.fields.DateField', [], {}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'grand_total': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sub_total': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'tip': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'total': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['MainApp']