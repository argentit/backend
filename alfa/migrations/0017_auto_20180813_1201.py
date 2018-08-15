# Generated by Django 2.0.7 on 2018-08-13 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alfa', '0016_charity_document_job'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-date']},
        ),
        migrations.RemoveField(
            model_name='service',
            name='about',
        ),
        migrations.AddField(
            model_name='service',
            name='description',
            field=models.CharField(default='', max_length=10000),
        ),
    ]
