# Generated by Django 2.2.3 on 2020-08-30 13:34

import datetime

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import recurrence.fields
from django.conf import settings
from django.db import migrations, models

import activity_calendar.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_presetimage'),
        ('activity_calendar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivitySlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('location', models.CharField(blank=True, help_text='If left empty, matches location with activity', max_length=255, null=True)),
                ('start_date', models.DateTimeField(blank=True, help_text='If left empty, matches start date with activity', null=True)),
                ('end_date', models.DateTimeField(blank=True, help_text='If left empty, matches end date with activity', null=True)),
                ('recurrence_id', models.DateTimeField(blank=True, help_text='If the activity is recurring, set this to the date/time of one of its occurences. Leave this field empty if the parent activity is non-recurring.', null=True, verbose_name='parent activity date/time')),
                ('max_participants', models.IntegerField(default=-1, help_text='-1 denotes unlimited participants', validators=[django.core.validators.MinValueValidator(-1)], verbose_name='maximum number of participants')),
                ('image', models.ForeignKey(blank=True, help_text='If left empty, matches the image of the activity.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='slot_image', to='core.PresetImage')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.ExtendedUser')),
            ],
        ),
        migrations.AlterModelOptions(
            name='activity',
            options={'verbose_name_plural': 'activities'},
        ),
        migrations.AddField(
            model_name='activity',
            name='end_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activity',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activity_image', to='core.PresetImage'),
        ),
        migrations.AddField(
            model_name='activity',
            name='last_updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='location',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activity',
            name='max_participants',
            field=models.IntegerField(default=-1, help_text='-1 denotes unlimited participants', validators=[django.core.validators.MinValueValidator(-1)]),
        ),
        migrations.AddField(
            model_name='activity',
            name='max_slots',
            field=models.IntegerField(default=1, help_text='-1 denotes unlimited slots', validators=[django.core.validators.MinValueValidator(-1)]),
        ),
        migrations.AddField(
            model_name='activity',
            name='max_slots_join_per_participant',
            field=models.IntegerField(default=1, help_text='-1 denotes unlimited slots', validators=[django.core.validators.MinValueValidator(-1)]),
        ),
        migrations.AddField(
            model_name='activity',
            name='recurrences',
            field=recurrence.fields.RecurrenceField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='activity',
            name='slot_creation',
            field=models.CharField(choices=[('CREATION_NONE', 'Never/By Administrators'), ('CREATION_AUTO', 'Automatically'), ('CREATION_USER', 'By Users')], default='CREATION_AUTO', max_length=15),
        ),
        migrations.AddField(
            model_name='activity',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activity',
            name='subscriptions_close',
            field=models.DurationField(default=datetime.timedelta(seconds=7200)),
        ),
        migrations.AddField(
            model_name='activity',
            name='subscriptions_open',
            field=models.DurationField(default=datetime.timedelta(days=7)),
        ),
        migrations.AddField(
            model_name='activity',
            name='subscriptions_required',
            field=models.BooleanField(default=True, help_text='People are only allowed to go to the activity if they register beforehand'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='activity',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='published_date',
            field=models.DateTimeField(default=activity_calendar.models.now_rounded),
        ),
        migrations.AlterField(
            model_name='activity',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('showed_up', models.BooleanField(default=None, help_text='Whether the participant actually showed up', null=True)),
                ('activity_slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activity_calendar.ActivitySlot')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ExtendedUser')),
            ],
        ),
        migrations.AddField(
            model_name='activityslot',
            name='parent_activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_activity', to='activity_calendar.Activity'),
        ),
        migrations.AddField(
            model_name='activityslot',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='participant_info', through='activity_calendar.Participant', to='core.ExtendedUser'),
        ),
    ]
