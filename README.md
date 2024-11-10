## иструкция по развертыванию

Сначала установите все контейнеры, которые в `compose.yml` файле.

После чего отредактируйте в корневой директории файл `.env`

```
POSTGRES_DB=fitin_db
POSTGRES_USER=fitin
POSTGRES_PASSWORD=fitinpassword

SECRET_KEY=django-insecure-%bhjy!m!468m!hw0he#
DEBUG=1

RABBITMQ_HOST=rabbitmq
REDIS_HOST=redis

EMAIL_HOST=
EMAIL_PORT=
EMAIL_USER=
EMAIL_PASSWORD=

DB_HOST=db
DB_PORT=5432

YOOKASSA_ID=
YOOKASSA_KEY=

```

После чего запустите команду
```
sudo docker compose up -d
```
