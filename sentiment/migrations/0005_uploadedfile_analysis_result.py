# Generated by Django 5.1.3 on 2024-11-24 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sentiment', '0004_uploadedfile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='analysis_result',
            field=models.TextField(blank=True, null=True),
        ),
    ]
