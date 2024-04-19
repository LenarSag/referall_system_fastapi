# referall_system_fastapi



В файле alembic.ini указываем адрес базы:

sqlalchemy.url = sqlite:///db.sqlite3

В файле alembic/env.py импортируем все модели и указываем target_metadata:

from db import Base

target_metadata = Base.metadata


Создаем файл миграции:

alembic revision --autogenerate -m 'initial'


Применяем миграции и создаем таблицу

alembic upgrade head