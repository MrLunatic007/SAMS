# Generated by Django 5.1.4 on 2024-12-23 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_start_date_assignments_due_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignments',
            name='file_name',
            field=models.FileField(upload_to='media'),
        ),
    ]
