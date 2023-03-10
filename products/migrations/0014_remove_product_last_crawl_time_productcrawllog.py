# Generated by Django 4.0.2 on 2022-05-09 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_category_icon_category_slider_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='last_crawl_time',
        ),
        migrations.CreateModel(
            name='ProductCrawlLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('crawl_time', models.DateTimeField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crawl_logs', to='products.product')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
