# Generated by Django 4.0.4 on 2023-02-12 17:30

import django.core.files.storage
from django.db import migrations
import user_authentication.models


class Migration(migrations.Migration):

    dependencies = [
        ('user_authentication', '0004_alter_userinformation_cropped_profile_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinformation',
            name='cropped_profile_image',
            field=user_authentication.models.CroppedImageImageField(null=True, storage=django.core.files.storage.FileSystemStorage(location='files/user_information/'), upload_to=''),
        ),
    ]
