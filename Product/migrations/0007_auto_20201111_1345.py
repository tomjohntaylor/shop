# Generated by Django 3.1.3 on 2020-11-11 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0006_auto_20201111_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='category_path',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='category_name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]