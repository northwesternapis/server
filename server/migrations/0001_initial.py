# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Term'
        db.create_table(u'server_term', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term_id', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('shopping_cart_date', self.gf('django.db.models.fields.DateField')()),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'server', ['Term'])

        # Adding model 'School'
        db.create_table(u'server_school', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('term', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['server.Term'])),
        ))
        db.send_create_signal(u'server', ['School'])

        # Adding model 'Subject'
        db.create_table(u'server_subject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['server.School'])),
            ('term', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['server.Term'])),
        ))
        db.send_create_signal(u'server', ['Subject'])

        # Adding model 'Instructor'
        db.create_table(u'server_instructor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('bio', self.gf('django.db.models.fields.TextField')(null=True)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('office_hours', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal(u'server', ['Instructor'])

        # Adding M2M table for field subject on 'Instructor'
        m2m_table_name = db.shorten_name(u'server_instructor_subject')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('instructor', models.ForeignKey(orm[u'server.instructor'], null=False)),
            ('subject', models.ForeignKey(orm[u'server.subject'], null=False))
        ))
        db.create_unique(m2m_table_name, ['instructor_id', 'subject_id'])

        # Adding model 'Course'
        db.create_table(u'server_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('term', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['server.Term'])),
            ('school', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('instructor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['server.Instructor'])),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('catalog_num', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('section', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('room', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('meeting_days', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('end_time', self.gf('django.db.models.fields.TimeField')()),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('seats', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('overview', self.gf('django.db.models.fields.TextField')(null=True)),
            ('topic', self.gf('django.db.models.fields.TextField')(null=True)),
            ('attributes', self.gf('django.db.models.fields.TextField')(null=True)),
            ('requirements', self.gf('django.db.models.fields.TextField')(null=True)),
            ('component', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('class_num', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('course_id', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
        ))
        db.send_create_signal(u'server', ['Course'])

        # Adding model 'CourseDesc'
        db.create_table(u'server_coursedesc', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['server.Course'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('desc', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'server', ['CourseDesc'])

        # Adding model 'CourseComponent'
        db.create_table(u'server_coursecomponent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('component', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('meeting_days', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('end_time', self.gf('django.db.models.fields.TimeField')()),
            ('section', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('room', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['server.Course'])),
        ))
        db.send_create_signal(u'server', ['CourseComponent'])


    def backwards(self, orm):
        # Deleting model 'Term'
        db.delete_table(u'server_term')

        # Deleting model 'School'
        db.delete_table(u'server_school')

        # Deleting model 'Subject'
        db.delete_table(u'server_subject')

        # Deleting model 'Instructor'
        db.delete_table(u'server_instructor')

        # Removing M2M table for field subject on 'Instructor'
        db.delete_table(db.shorten_name(u'server_instructor_subject'))

        # Deleting model 'Course'
        db.delete_table(u'server_course')

        # Deleting model 'CourseDesc'
        db.delete_table(u'server_coursedesc')

        # Deleting model 'CourseComponent'
        db.delete_table(u'server_coursecomponent')


    models = {
        u'server.course': {
            'Meta': {'object_name': 'Course'},
            'attributes': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'catalog_num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'class_num': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'component': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'course_id': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.Instructor']"}),
            'meeting_days': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'overview': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'requirements': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'seats': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.Term']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'topic': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        u'server.coursecomponent': {
            'Meta': {'object_name': 'CourseComponent'},
            'component': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.Course']"}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meeting_days': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'start_time': ('django.db.models.fields.TimeField', [], {})
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
            'subject': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['server.Subject']", 'symmetrical': 'False'})
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
            'term_id': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        }
    }

    complete_apps = ['server']