# Generated by Django 3.1.3 on 2020-11-13 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0024_auto_20201113_1026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productcategory',
            name='attributes',
        ),
        migrations.RemoveField(
            model_name='productcategory',
            name='attributes_old',
        ),
    ]
