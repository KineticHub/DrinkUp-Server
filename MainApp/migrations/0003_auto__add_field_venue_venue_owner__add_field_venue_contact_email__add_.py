# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Venue.venue_owner'
        db.add_column('MainApp_venue', 'venue_owner',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['MainApp.VenueOwner']),
                      keep_default=False)

        # Adding field 'Venue.contact_email'
        db.add_column('MainApp_venue', 'contact_email',
                      self.gf('django.db.models.fields.EmailField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'Venue.contact_number'
        db.add_column('MainApp_venue', 'contact_number',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default='0', blank=True),
                      keep_default=False)

        # Adding field 'AppUser.password_salt'
        db.add_column('MainApp_appuser', 'password_salt',
                      self.gf('django.db.models.fields.CharField')(default='salty', max_length=255),
                      keep_default=False)

        # Adding field 'AppUser.password_hash'
        db.add_column('MainApp_appuser', 'password_hash',
                      self.gf('django.db.models.fields.CharField')(default='hashy', max_length=255),
                      keep_default=False)

        # Deleting field 'VenueOwner.password_hash'
        db.delete_column('MainApp_venueowner', 'password_hash')

        # Deleting field 'VenueOwner.password_salt'
        db.delete_column('MainApp_venueowner', 'password_salt')

        # Deleting field 'VenueOwner.venue'
        db.delete_column('MainApp_venueowner', 'venue_id')


    def backwards(self, orm):
        # Deleting field 'Venue.venue_owner'
        db.delete_column('MainApp_venue', 'venue_owner_id')

        # Deleting field 'Venue.contact_email'
        db.delete_column('MainApp_venue', 'contact_email')

        # Deleting field 'Venue.contact_number'
        db.delete_column('MainApp_venue', 'contact_number')

        # Deleting field 'AppUser.password_salt'
        db.delete_column('MainApp_appuser', 'password_salt')

        # Deleting field 'AppUser.password_hash'
        db.delete_column('MainApp_appuser', 'password_hash')


        # User chose to not deal with backwards NULL issues for 'VenueOwner.password_hash'
        raise RuntimeError("Cannot reverse this migration. 'VenueOwner.password_hash' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'VenueOwner.password_salt'
        raise RuntimeError("Cannot reverse this migration. 'VenueOwner.password_salt' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'VenueOwner.venue'
        raise RuntimeError("Cannot reverse this migration. 'VenueOwner.venue' and its values cannot be restored.")

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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password_hash': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password_salt': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'MainApp.drink': {
            'Meta': {'ordering': "['name']", 'object_name': 'Drink'},
            'bar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['MainApp.VenueBar']"}),
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
            'bar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['MainApp.VenueBar']"}),
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
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            'contact_number': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'foursquare_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'icon': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'venue_owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['MainApp.VenueOwner']"})
        },
        'MainApp.venuebar': {
            'Meta': {'ordering': "['name']", 'object_name': 'VenueBar'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'happyhour_end': ('django.db.models.fields.DateTimeField', [], {}),
            'happyhour_start': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['MainApp.Venue']"})
        },
        'MainApp.venueowner': {
            'Meta': {'object_name': 'VenueOwner'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.PositiveIntegerField', [], {}),
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
