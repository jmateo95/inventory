# Generated by Django 3.2.4 on 2021-10-03 23:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_groupproduct_productsuplier_producttype_saleprice_suplier'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producttype',
            old_name='reorderpoint',
            new_name='orderquantity',
        ),
    ]