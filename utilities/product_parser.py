
import decimal
from dis import dis
from fractions import Fraction
from django.db import transaction
from uuid import uuid4
import os
import json
import argparse
import re

# fmt: off
from restoxa import setup
setup()

from shops.models import Shop
from products.models import CurrencyChoice, Product, ProductCrawlLog, ProductPriceLog
# fmt: on

parser = argparse.ArgumentParser()
parser.add_argument("file_path", help="Products json file path")

args = parser.parse_args()

current_path = os.getcwd()

with open(args.file_path, 'r') as file:
    j_root = json.loads(file.read())

    j_products = j_root['products']
    j_shop = j_root['shop']

    shop_name = j_shop['sitename']
    shop_country = j_shop['country']
    shop_link = j_shop['site_address']

    try:
        shop = Shop.objects.get(
            name=shop_name, country=shop_country, link=shop_link)

    except Shop.DoesNotExist:
        should_create = input(
            f'Shop "{shop_name}" not found. Do you wanna create it ?')
        if 'y' in should_create:
            shop = Shop()
            shop.name = shop_name
            shop.country = shop_country
            shop.link = shop_link
            shop.save()
            print("Shop created successfully")
        else:
            exit(0)

    updated_products_count = 0
    inserted_products_count = 0

    with transaction.atomic():

        for j_product in j_products:

            is_new = False

            try:
                product: Product = Product.objects.get(
                    name=j_product['name'], shop__name=shop.name)

                price = decimal.Decimal(str(j_product['price']))
                discount = decimal.Decimal(str(j_product['discount']))

                if price != product.price or product.discount != discount:
                    price_log = ProductPriceLog()
                    price_log.product = product
                    price_log.price = price
                    price_log.discount = discount
                    price_log.save()

            except Product.DoesNotExist:
                product = Product()
                product.uuid = uuid4()
                is_new = True

            product.name = j_product['name']
            product.brand = j_product.get('brand')
            product.link = j_product['link']
            product.price = j_product['price']
            product.currency = CurrencyChoice[j_product['currency']]
            product.tags = j_product['tags']
            product.enable = j_product['enable']
            product.discount = j_product['discount']
            product.original_image = j_product['image']
            product.description = j_product.get('description')
            product.color = j_product.get('color')
            product.shop = shop

            slug_pattern = re.compile("(\s|_|\(|\)|\t|\||\/)")

            str_name = str(product.name)

            slug_name = str_name if len(str_name) <= 40 else str_name[0:40]

            product.slug = re.sub(
                slug_pattern, "-", slug_name +
                '-' + str(product.uuid)[0:5]).replace('--', '-')

            product.save()

            crawl_log = ProductCrawlLog()
            crawl_log.crawl_id = j_product.get('id')
            crawl_log.product = product
            crawl_log.crawl_time = j_product['updated_at']
            crawl_log.save()

            if is_new:
                inserted_products_count += 1
            else:
                updated_products_count += 1

    print(f"{inserted_products_count} Products inserted.")
    print(f"{updated_products_count} Products updated.")
