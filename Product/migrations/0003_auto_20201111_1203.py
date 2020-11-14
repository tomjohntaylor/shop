# Generated by Django 3.1.3 on 2020-11-11 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0002_productcategory_root_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_category',
            field=models.ForeignKey(limit_choices_to={'is_root': False}, on_delete=django.db.models.deletion.CASCADE, to='Product.productcategory'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='atr_color',
            field=models.CharField(blank=True, choices=[('BLUE', 'Blue'), ('RED', 'Red')], max_length=50),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='atr_length',
            field=models.FloatField(blank=True),
        ),
    ]