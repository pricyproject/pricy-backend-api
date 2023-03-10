# Generated by Django 4.0.5 on 2022-07-08 21:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0027_product_short_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductLinkView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client_ip', models.GenericIPAddressField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='link_views', to='products.product')),
            ],
            options={
                'verbose_name_plural': 'Product Link Views',
            },
        ),
    ]
