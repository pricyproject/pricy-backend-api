# Generated by Django 4.0.2 on 2022-06-05 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_remove_productview_session_id_productview_client_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(related_name='products', to='products.Category'),
        ),
    ]
