# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Course.room'
        db.alter_column(u'server_course', 'room', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

    def backwards(self, orm):

        # Changing field 'Course.room'
        db.alter_column(u'server_course', 'room', self.gf('django.db.models.fields.CharField')(default=None, max_length=50))

    models = {
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
            'meeting_days': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True'}),
            'overview': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'requirements': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'seats': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'null': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.Term']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'topic': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        u'server.coursecomponent': {
            'Meta': {'object_name': 'CourseComponent'},
            'component': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.Course']"}),
            'end_time': ('django.db.models.fields.TimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meeting_days': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'null': 'True'})
        },
        u'server.coursedesc': {
            'Meta': {'object_name': 'CourseDesc'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.Course']"}),
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
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['server.Subject']", 'symmetrical': 'False'})
        },
        u'server.school': {
            'Meta': {'object_name': 'School'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.Term']"})
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