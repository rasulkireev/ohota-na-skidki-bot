# Generated by Django 5.0.6 on 2024-07-06 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.TextField(),
        ),
    ]
