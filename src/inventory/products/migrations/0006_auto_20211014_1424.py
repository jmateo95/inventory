# Generated by Django 3.2.4 on 2021-10-14 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_order_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='validation_key',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.CharField(default='No Completado', max_length=200),
        ),
    ]
