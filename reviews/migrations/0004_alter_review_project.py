# Generated by Django 4.0.4 on 2023-04-01 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0016_alter_project_project_file'),
        ('reviews', '0003_alter_comment_image_comment_alter_comment_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='project',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
        ),
    ]
