# Описание

## API сервис для реферальной системы.

Регистрация и аутентификация пользователя (JWT, Oauth 2.0). Аутентифицированный пользователь  имеет возможность создать или удалить свой реферальный код. Одновременно может быть активен только 1 код. При создании кода обязательно должен быть задан его срок годности.
Возможно получеить реферального кода по email адресу реферера.
Возможна регистрации по реферальному коду в качестве реферала.
Получение информации о рефералах по id реферера.

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

git clone https://github.com/LenarSag/referall_system_fastapi

cd referall_system_fastapi

Cоздать и активировать виртуальное окружение:

python3 -m venv env

source env/bin/activate

Установить зависимости из файла requirements.txt:

python3 -m pip install --upgrade pip

pip install -r requirements.txt

Создаем файл миграции:

alembic revision --autogenerate -m 'initial'

Применяем миграции и создаем таблицу:

alembic upgrade head

Запускаем проект:

python3 main.py


Документация доступна по адресу  http://127.0.0.1:8000/docs/