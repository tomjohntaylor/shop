# Generated by Django 3.1.3 on 2020-11-13 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0022_auto_20201113_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='attributes_json',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='attributes_json',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='attributes_old',
            field=models.JSONField(default=dict, editable=False),
        ),
    ]
