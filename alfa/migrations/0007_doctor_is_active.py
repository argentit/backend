# Generated by Django 2.0.7 on 2018-07-11 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alfa', '0006_auto_20180709_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
