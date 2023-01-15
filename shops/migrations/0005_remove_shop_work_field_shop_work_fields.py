# Generated by Django 4.0.2 on 2022-06-05 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0004_alter_shop_options_alter_shopworkfield_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='work_field',
        ),
        migrations.AddField(
            model_name='shop',
            name='work_fields',
            field=models.ManyToManyField(related_name='shops', to='shops.ShopWorkField'),
        ),
    ]
