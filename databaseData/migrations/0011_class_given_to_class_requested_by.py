# Generated by Django 5.1.3 on 2024-12-29 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databaseData', '0010_alter_scheduler_class_department_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='given_to',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='class',
            name='requested_by',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
