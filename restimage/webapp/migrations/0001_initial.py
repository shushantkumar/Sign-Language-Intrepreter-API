# Generated by Django 2.0.1 on 2018-02-18 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=140)),
                ('opening', models.FloatField()),
                ('close', models.FloatField()),
                ('volume', models.IntegerField()),
            ],
        ),
    ]
