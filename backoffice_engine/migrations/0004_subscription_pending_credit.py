# Generated by Django 5.2.1 on 2025-06-18 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice_engine', '0003_plandetails_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='pending_credit',
            field=models.IntegerField(default=5),
        ),
    ]
