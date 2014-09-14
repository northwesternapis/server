# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
import sys

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.

        # NOTE: This is handwritten migration code
        # Must manually add the line to models.py in the Course model:
        #   room = models.CharField(max_length=50, null=True)
        # then remove it when you're done

        # Load all of the StringRoomMappings into a dictionary
        mappings = {}
        for mapping in orm.StringRoomMapping.objects.iterator():
            mappings[mapping.orig_string] = mapping.room

        # Translate classroom data from strings to foreignkeys
        for course in orm.Course.objects.iterator():
            if course.room_temp == None:
                # If there was no data, leave the foreignkey null for now
                course.room = None
                course.save()
                continue

            try:
                room = mappings[course.room_temp]
            except:
                print course.id
                print course.title
                print course.subject
                print course.term.term_id
                print course.room_temp
                sys.exit() # immediately quit
            course.room = room
            course.save()
            #print course.id, course.title, course.room.full_name, course.room_temp

        # Add an index on room id
        db.create_index(u'server_course', ['room_id'])

        # Delete the old column
        db.delete_column(u'server_course', 'room_temp')


    def backwards(self, orm):
        # Add temporary column
        db.add_column(u'server_course', 'room', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Delete an index on room id
        db.delete_index(u'server_course', ['room'])

        # Translate classroom data from foreignkeys to strings
        for course in orm.Course.objects.iterator():
            mapping = orm.StringRoomMapping.objects.get(
                                room=course.room)
            course.room_temp = mapping.orig_string
            course.save()

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
        },
        u'server.allowedreferrer': {
            'APIProject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.APIProject']"}),
            'Meta': {'object_name': 'AllowedReferrer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        u'server.apiproject': {
            'Meta': {'object_name': 'APIProject'},
            'api_key': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects_approved'", 'to': u"orm['auth.User']"}),
            'daily_limit': ('django.db.models.fields.IntegerField', [], {'default': '10000'}),
            'date_approved': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'original_request': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.APIProjectRequest']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'api_projects'", 'to': u"orm['auth.User']"}),
            'requests_sent': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'server.apiprojectrequest': {
            'Meta': {'object_name': 'APIProjectRequest'},
            'date_submitted': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'how_long': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'S'", 'max_length': '1'})
        },
        u'server.building': {
            'Meta': {'object_name': 'Building'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'nu_maps_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'server.course': {
            'Meta': {'object_name': 'Course'},
            'attributes': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'catalog_num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'class_num': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'component': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'course_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'end_time': ('django.db.models.fields.TimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.Instructor']"}),
            'meeting_days': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'overview': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'requirements': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.Room']", 'null': 'True'}),
            'room_temp': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'seats': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'null': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.Term']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'topic': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        u'server.coursecomponent': {
            'Meta': {'object_name': 'CourseComponent'},
            'component': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'course_components'", 'to': u"orm['server.Course']"}),
            'end_time': ('django.db.models.fields.TimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meeting_days': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'null': 'True'})
        },
        u'server.coursedesc': {
            'Meta': {'object_name': 'CourseDesc'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'course_descriptions'", 'to': u"orm['server.Course']"}),
            'desc': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'server.instructor': {
            'Meta': {'object_name': 'Instructor'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'office_hours': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['server.Subject']", 'symmetrical': 'False'})
        },
        u'server.room': {
            'Meta': {'object_name': 'Room'},
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.Building']"}),
            'full_name': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        u'server.school': {
            'Meta': {'object_name': 'School'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.Term']"})
        },
        u'server.scraperecord': {
            'Meta': {'object_name': 'ScrapeRecord'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.School']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.Subject']"}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.Term']"})
        },
        u'server.stringroommapping': {
            'Meta': {'object_name': 'StringRoomMapping'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orig_string': ('django.db.models.fields.TextField', [], {}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.Room']"})
        },
        u'server.subject': {
            'Meta': {'object_name': 'Subject'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.School']"}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.Term']"})
        },
        u'server.term': {
            'Meta': {'object_name': 'Term'},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'shopping_cart_date': ('django.db.models.fields.DateField', [], {}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'term_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['server']
    symmetrical = True
