# Generated by Django 4.0.2 on 2022-03-08 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_alter_product_discount_alter_product_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.CharField(default='', max_length=1024),
        ),
    ]
