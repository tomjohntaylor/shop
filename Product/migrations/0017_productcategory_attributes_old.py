# Generated by Django 3.1.3 on 2020-11-13 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0016_auto_20201112_2145'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='attributes_old',
            field=models.TextField(default='', editable=False),
        ),
    ]