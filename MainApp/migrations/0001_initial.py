# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Venue'
        db.create_table('MainApp_venue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('icon', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('facebook_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('foursquare_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('MainApp', ['Venue'])

        # Adding model 'Venue_Owner'
        db.create_table('MainApp_venue_owner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['MainApp.Venue'])),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('phone', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('password_salt', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('password_hash', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('MainApp', ['Venue_Owner'])

        # Adding model 'Venue_Bar'
        db.create_table('MainApp_venue_bar', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['MainApp.Venue'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('happyhour_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('happyhour_end', self.gf('django.db.models.fields.DateTimeField')()),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('MainApp', ['Venue_Bar'])

        # Adding model 'Drink'
        db.create_table('MainApp_drink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('bar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['MainApp.Venue_Bar'])),
            ('drink_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['MainApp.DrinkType'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('happyhour_price', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('MainApp', ['Drink'])

        # Adding model 'DrinkType'
        db.create_table('MainApp_drinktype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('type_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('MainApp', ['DrinkType'])

        # Adding model 'Order'
        db.create_table('MainApp_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('bar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['MainApp.Venue_Bar'])),
            ('appuser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['MainApp.AppUser'])),
            ('total', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('tax', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('sub_total', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('tip', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('fees', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
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
            ('ordered_during_happyhour', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('MainApp', ['DrinkOrdered'])

        # Adding model 'AppUser'
        db.create_table('MainApp_appuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('birthdate', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('facebook_user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['MainApp.FacebookAppUser'], unique=True, null=True, blank=True)),
            ('foursquare_user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['MainApp.FourSquareAppUser'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('MainApp', ['AppUser'])

        # Adding model 'FacebookAppUser'
        db.create_table('MainApp_facebookappuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('fb_uid', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('fb_email', self.gf('django.db.models.fields.EmailField')(max_length=255, blank=True)),
            ('oauth_token', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['MainApp.OAuthToken'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('MainApp', ['FacebookAppUser'])

        # Adding model 'FourSquareAppUser'
        db.create_table('MainApp_foursquareappuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('fs_uid', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('fs_email', self.gf('django.db.models.fields.EmailField')(max_length=255, blank=True)),
            ('oauth_token', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['MainApp.OAuthToken'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('MainApp', ['FourSquareAppUser'])

        # Adding model 'OAuthToken'
        db.create_table('MainApp_oauthtoken', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('token', self.gf('django.db.models.fields.TextField')()),
            ('issued_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('expires_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('MainApp', ['OAuthToken'])


    def backwards(self, orm):
        # Deleting model 'Venue'
        db.delete_table('MainApp_venue')

        # Deleting model 'Venue_Owner'
        db.delete_table('MainApp_venue_owner')

        # Deleting model 'Venue_Bar'
        db.delete_table('MainApp_venue_bar')

        # Deleting model 'Drink'
        db.delete_table('MainApp_drink')

        # Deleting model 'DrinkType'
        db.delete_table('MainApp_drinktype')

        # Deleting model 'Order'
        db.delete_table('MainApp_order')

        # Deleting model 'DrinkOrdered'
        db.delete_table('MainApp_drinkordered')

        # Deleting model 'AppUser'
        db.delete_table('MainApp_appuser')

        # Deleting model 'FacebookAppUser'
        db.delete_table('MainApp_facebookappuser')

        # Deleting model 'FourSquareAppUser'
        db.delete_table('MainApp_foursquareappuser')

        # Deleting model 'OAuthToken'
        db.delete_table('MainApp_oauthtoken')


    models = {
        'MainApp.appuser': {
            'Meta': {'ordering': "['email']", 'object_name': 'AppUser'},
            'birthdate': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'facebook_user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['MainApp.FacebookAppUser']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'foursquare_user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['MainApp.FourSquareAppUser']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'MainApp.drink': {
            'Meta': {'ordering': "['name']", 'object_name': 'Drink'},
            'bar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['MainApp.Venue_Bar']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'drink_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['MainApp.DrinkType']"}),
            'happyhour_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
            'ordered_during_happyhour': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'unit_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'})
        },
        'MainApp.drinktype': {
            'Meta': {'ordering': "['type_name']", 'object_name': 'DrinkType'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'MainApp.facebookappuser': {
            'Meta': {'object_name': 'FacebookAppUser'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'fb_email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            'fb_uid': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oauth_token': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['MainApp.OAuthToken']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'MainApp.foursquareappuser': {
            'Meta': {'object_name': 'FourSquareAppUser'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'fs_email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            'fs_uid': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
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
            'Meta': {'ordering': "['created']", 'object_name': 'Order'},
            'appuser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['MainApp.AppUser']"}),
            'bar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['MainApp.Venue_Bar']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fees': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'grand_total': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sub_total': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'tip': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'total': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'MainApp.venue': {
            'Meta': {'object_name': 'Venue'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'foursquare_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'icon': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'MainApp.venue_bar': {
            'Meta': {'ordering': "['name']", 'object_name': 'Venue_Bar'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'happyhour_end': ('django.db.models.fields.DateTimeField', [], {}),
            'happyhour_start': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['MainApp.Venue']"})
        },
        'MainApp.venue_owner': {
            'Meta': {'object_name': 'Venue_Owner'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password_hash': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password_salt': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['MainApp.Venue']"})
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