# Generated by Django 3.2.4 on 2021-10-03 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20211003_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producttype',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]