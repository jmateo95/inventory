# Generated by Django 3.2.4 on 2021-10-09 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='nit',
            field=models.BigIntegerField(null=True, unique=True),
        ),
    ]
