# Generated by Django 3.1.3 on 2020-11-15 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SaleProcess', '0003_auto_20201115_1427'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='session',
        ),
    ]
