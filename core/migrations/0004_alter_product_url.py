# Generated by Django 5.0.6 on 2024-07-06 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_product_price_alter_product_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='url',
            field=models.URLField(max_length=500),
        ),
    ]
