# Generated by Django 4.0.2 on 2022-05-09 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.CharField(blank=True, max_length=512),
        ),
        migrations.AddField(
            model_name='category',
            name='slider_image',
            field=models.CharField(blank=True, max_length=512),
        ),
    ]
