# Generated by Django 3.1.2 on 2020-10-20 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statsgetter', '0002_auto_20201019_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistics',
            name='view_count',
            field=models.BigIntegerField(default=0),
        ),
    ]
