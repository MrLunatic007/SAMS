# Generated by Django 5.1.4 on 2024-12-23 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_assignments_file_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignments',
            name='file_name',
            field=models.FileField(upload_to='media/'),
        ),
    ]
