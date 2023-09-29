# Generated by Django 2.2.15 on 2021-08-22 17:37

from django.db import migrations, models

import core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('roleplaying', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='roleplayingsystem',
            name='more_info_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='roleplayingsystem',
            name='dice',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='roleplayingsystem',
            name='long_description',
            field=core.fields.MarkdownTextField(blank=True, null=True),
        ),
    ]
