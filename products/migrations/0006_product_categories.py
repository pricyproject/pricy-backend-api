# Generated by Django 4.0.2 on 2022-03-02 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_product_brand_digitalcategory_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(to='products.Category'),
        ),
    ]
