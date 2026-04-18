# Sandboxes

Two sandboxes are included for manual functional testing. They are **not** part of the published PyPI package.

## sandbox/django52

Django 5.2 sandbox.

```bash
cd sandbox/django52
cp .env.example .env
# Edit .env with your SUAP credentials
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## sandbox/django60

Django 6.0 sandbox.

```bash
cd sandbox/django60
cp .env.example .env
# Edit .env with your SUAP credentials
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Comparing Django Versions

The two sandboxes allow you to compare the behavior of django-suap-auth across Django 5.2 and 6.0. Both are configured identically and use the same package code from the parent directory.
