# Generated by Django 5.1.4 on 2024-12-23 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_assignments_file_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignments',
            name='file_name',
            field=models.FileField(upload_to='media/'),
        ),
    ]
