# Generated by Django 4.0.4 on 2023-01-30 12:28

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_project_id_alter_project_publisher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/files/projects'), upload_to=''),
        ),
    ]
