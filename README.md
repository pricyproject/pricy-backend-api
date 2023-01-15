# site-frontend

Django Front-End


## Installation

At the moment we are using `PostgreSQL` as DB. To install postgresql in Debian based systems run the following command:

```bash
sudo apt install postgresql
```

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```


#### Change default credentials:
```bash
cp .env.sample .env
```
Add your new credentials into `.env` file.

#### Suffering from lack of the SECRET_KEY?
```bash
python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'
```

## Run server

```console
python manage.py runserver 6000
```

## API Docs

```console
Swagger API:
http://127.0.0.1:8000/api/schema/swagger-ui/

Redoc API:
http://127.0.0.1:8000/api/schema/redoc/
```

## Flexible Query Parameters

- `include={related1,related2,...}` - Get related model field(s) included in response object(s)
- `fields={field1,field2,...}` - Get specific field(s) of object(s) only
- `omit={field1,field2,...}` - Exclude specific field(s) from object(s)

```
Examples:

http://127.0.0.1:8000/api/products/?include=shop,groups

http://127.0.0.1:8000/api/products/?fields=id,name

http://127.0.0.1:8000/api/products/?omit=shop,uuid
```