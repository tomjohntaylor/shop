# Generated by Django 3.1.3 on 2020-11-15 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SaleProcess', '0006_auto_20201115_1519'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='products_json',
            new_name='cart_json',
        ),
    ]