# Generated by Django 3.1.3 on 2020-11-13 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0026_remove_product_attributes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='attributes_json',
            field=models.JSONField(default={'brak danych': None}),
        ),
    ]