### tg_bot_testovoe
```
Стек:

1)aiogram
2)SQLAlchemy 1.4+
3)PostgreSQL as database
4)Docker с docker-compose
```

## Установка и запуск

1. Склонировать репозиторий с Github:

````
git clone git@github.com:Sapik-pyt/tg_bot_testovoe.git
````
2. Перейти в директорию проекта
/tg_bot_testovoe
````
cd tg_bot_testovoe/
````
3. Создать виртуальное окружение:

````
python -3.9 -m venv venv
````

4. Активировать окружение: 

````
source \venv\Scripts\activate
````
5. Файл .env.example переименовать в .env
   Заполнить все недостающие поля
````
6. Установка зависимостей:

```
pip install -r requirements.txt
```

## Установка проекта с помощью Docker
```
1. Склонировать репозиторий с Github
```
git clone git@github.com:Sapik-pyt/notification-service.git
```
2. Перейти в директорию проекта
3. Файл .env.example переименовать в .env и изменить данные в нем на подходящие вам 
4. Запустить контейнеры 
``` 
sudo docker-compose up -d
 ```
