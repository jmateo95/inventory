# Generated by Django 3.2.4 on 2021-10-16 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_supplier_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
