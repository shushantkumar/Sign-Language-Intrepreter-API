# Generated by Django 2.0.1 on 2018-02-19 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='image',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
