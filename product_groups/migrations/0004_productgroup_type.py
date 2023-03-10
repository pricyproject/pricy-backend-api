# Generated by Django 4.0.2 on 2022-06-17 05:59

from django.db import migrations, models
import product_groups.models


class Migration(migrations.Migration):

    dependencies = [
        ('product_groups', '0003_alter_productgroup_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='productgroup',
            name='type',
            field=models.CharField(choices=[(product_groups.models.ProductGroupType['Normal'], 'Normal'), (product_groups.models.ProductGroupType['Featured'], 'Featured')], default=product_groups.models.ProductGroupType['Normal'], max_length=32),
        ),
    ]
