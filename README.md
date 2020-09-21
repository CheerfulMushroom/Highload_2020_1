# Highload_2020_1

## Описание

Архитектура сервер - prefork + coroutines.

- открывается сокет
- создается заданное количество рабочих процессов, каждый из которых слушает сокет
- как только процесс получает клиента по скоету, создаётся корутина, которая будет обслуживать клиента

## Подготовка

- Проинициализировать сабмодуль http-test-suite

``git submodule update --init --recursive``

- Скопировать http-test-suite/httptest/ в nginx/

``cp -r http-test-suite/httptest nginx``

## Тестирование

- чтобы запустить сервер

``sudo docker build -t pythonserver . && sudo docker run -p 80:3000 pythonserver``

- чтобы запустить nginx

``sudo docker build -t pythonserver:nginx ./nginx &&  sudo docker run -p 80:3000 pythonserver:nginx``



