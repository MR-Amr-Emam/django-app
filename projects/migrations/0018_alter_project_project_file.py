# Generated by Django 4.0.4 on 2023-07-21 20:19

import django.core.files.storage
from django.db import migrations
import projects.models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_alter_project_project_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_file',
            field=projects.models.ProjectFileField(storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\User\\Desktop\\projects\\educational website project-assignment\\django-app\\files/projects'), upload_to=''),
        ),
    ]