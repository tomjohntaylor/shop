# Generated by Django 3.1.3 on 2020-11-11 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0013_remove_productcategory_category_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='category_path',
            field=models.CharField(default=None, editable=False, max_length=300),
        ),
    ]