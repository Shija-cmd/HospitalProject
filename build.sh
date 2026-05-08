#!/usr/bin/env bash

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate

python manage.py createsupperuser \
	--noinput \
	--username admin \
	--email shijajuma@gmail.com || true
