# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field instructors on 'Course'
        m2m_table_name = db.shorten_name(u'server_course_instructors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm[u'server.course'], null=False)),
            ('instructor', models.ForeignKey(orm[u'server.instructor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['course_id', 'instructor_id'])

        # Copy data from the instructor ForeignKey to the instructors ManyToManyField
        for course in orm.Course.objects.iterator():
            course.instructors.add(course.instructor)
            course.save()


    def backwards(self, orm):
        # Removing M2M table for field instructors on 'Course'
        db.delete_table(db.shorten_name(u'server_course_instructors'))


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
            'Meta': {'object_name': 'AllowedReferrer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.APIProject']"}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        u'server.apiproject': {
            'Meta': {'object_name': 'APIProject'},
            'api_key': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects_approved'", 'to': u"orm['auth.User']"}),
            'daily_limit': ('django.db.models.fields.IntegerField', [], {'default': '10000'}),
            'date_approved': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
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
            'instructors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'courses'", 'symmetrical': 'False', 'to': u"orm['server.Instructor']"}),
            'meeting_days': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'overview': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'requirements': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.Room']", 'null': 'True'}),
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
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.Subject']"})
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
