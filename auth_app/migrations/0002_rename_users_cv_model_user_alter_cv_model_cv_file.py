# Generated by Django 5.1.1 on 2024-10-10 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cv_model',
            old_name='users',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='cv_model',
            name='cv_file',
            field=models.FileField(upload_to='uploads/cvs/'),
        ),
    ]
