# Generated by Django 3.1.3 on 2020-11-13 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0025_auto_20201113_1031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='attributes',
        ),
    ]
