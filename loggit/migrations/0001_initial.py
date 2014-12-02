# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone
import loggit.models

import swapper


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_ts', models.DateTimeField(default=django.utils.timezone.now)),
                ('actor', models.ForeignKey(related_name="(classname){u'class': 'logentry', u'app_label': 'loggit'}", blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
                'swappable': swapper.swappable_setting('loggit', 'LogEntry'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LogEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('template', models.TextField()),
            ],
            options={
                'abstract': False,
                'swappable': swapper.swappable_setting('loggit', 'LogEvent'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RelatedObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.IntegerField(db_index=True)),
                ('label', models.CharField(max_length=255)),
                ('content_type', models.ForeignKey(related_name='related_relatedobject', to='contenttypes.ContentType')),
                ('log_entry', models.ForeignKey(related_name='log_entries', to=swapper.get_model_name('loggit', 'LogEntry'))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='logentry',
            name='event',
            field=models.ForeignKey(related_name="(classname){u'class': 'logentry', u'app_label': 'loggit'}", to=swapper.get_model_name('loggit', 'LogEvent')),
            preserve_default=True,
        ),
    ]
