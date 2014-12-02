# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import swapper


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_ts', models.DateTimeField(default=django.utils.timezone.now)),
                ('actor', models.ForeignKey(related_name='log_entries', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
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
        migrations.AddField(
            model_name='logentry',
            name='event',
            field=models.ForeignKey(related_name='events', to=swapper.get_model_name('loggit', 'LogEvent')),
            preserve_default=True,
        ),
    ]
