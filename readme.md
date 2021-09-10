# Инструкция

## Запуск
docker run --env-file ./envfile -v routes.csv:/app/  python-docker

## Env variables

MYSQL_USER=root

MYSQL_PASSWORD=123456

MYSQL_HOST=192.168.1.10

MYSQL_DATABASE=test_db

MYSQL_PORT=8080

YANDEX_API_KEY=873bb74e-d3d0-400e-8557-dc012b185111

CSV_ROUTE_FILE=./routes.csv

IMPORT_DAYS=10

