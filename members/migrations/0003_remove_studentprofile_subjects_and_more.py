# Generated by Django 5.0.7 on 2025-03-03 22:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_class_customuser_is_parent_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentprofile',
            name='subjects',
        ),
        migrations.RemoveField(
            model_name='teacherprofile',
            name='subjects_taught',
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='subjects',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='members.subjects'),
        ),
        migrations.AddField(
            model_name='teacherprofile',
            name='subjects_taught',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='members.subjects'),
        ),
    ]
