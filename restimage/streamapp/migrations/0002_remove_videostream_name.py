# Generated by Django 2.0.1 on 2018-03-12 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streamapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videostream',
            name='name',
        ),
    ]
