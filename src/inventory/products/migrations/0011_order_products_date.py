# Generated by Django 3.2.4 on 2021-10-20 16:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_merge_20211018_2131'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_products',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]