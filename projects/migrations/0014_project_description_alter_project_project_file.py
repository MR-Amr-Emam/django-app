# Generated by Django 4.0.4 on 2023-02-02 13:15

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0013_project_publisher'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
