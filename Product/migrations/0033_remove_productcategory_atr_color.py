# Generated by Django 3.1.3 on 2020-11-13 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0032_auto_20201113_1142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productcategory',
            name='atr_color',
        ),
    ]
