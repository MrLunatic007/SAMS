# Generated by Django 5.2 on 2025-04-05 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_remove_teacherprofile_subjects_taught_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentprofile',
            name='subjects',
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='subjects',
            field=models.ManyToManyField(blank=True, to='members.subjects'),
        ),
    ]
