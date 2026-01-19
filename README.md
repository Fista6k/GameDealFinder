# GameDealFinder
GameDealFinder — это Django-приложение для отслеживания цен на игры в разных магазинах с возможностью добавления игр в вейтлист и получения email-уведомлений при достижении желаемой цены.

## Технологии
Python 3.13.9
Django 6.0
requests 2.32.5
Postgres 18
## Скриншоты страниц
Главная страница
  Здесь можно видеть список различных игр
  <img width="1903" height="869" alt="image" src="https://github.com/user-attachments/assets/daa3f6e7-9473-4deb-82aa-3f91068f59fc" />

Страница игры
  Здесь можно ознакомиться с ценами в разных магазинах и добавить игру в лист ожидания (вейтлист)
  <img width="1897" height="853" alt="image" src="https://github.com/user-attachments/assets/4817ccc8-bf49-42ee-8083-5e8e9436e302" />

Страница профиля
  Здесь можно посмотреть свою информацию, включая ваш вейтлист
  <img width="1916" height="457" alt="image" src="https://github.com/user-attachments/assets/5ae94f5c-7cef-4e9d-b604-04c3b77b70ce" />

Страница вейтлиста
  Здесь можно видеть игры, которые были добавлены в лист ожидания
  <img width="1917" height="689" alt="image" src="https://github.com/user-attachments/assets/77010f98-4a4c-4413-9765-74f43b24e496" />
  <img width="1919" height="762" alt="image" src="https://github.com/user-attachments/assets/75aaa460-a276-4f97-bea0-9fdb9655cf91" />


## Установка и запуск
1. Клонировать репозиторий
https://github.com/Fista6k/GameDealFinder.git

2. Создать виртуальное окружение
python -m venv venv
venv\Scripts\activate

3. Установить зависимости
pip install -r requirements.txt

4. Задать переменные окружения
   4.1 Создать в корне проекта файл .env
   4.2 В этом файле задать следующие переменные:
     SECRET_KEY - ключ, которые генерируется при создании проекта (по дефолту должен находиться в файле settings.py)
     ALLOWED_HOST - список доменов, с которых Django позволяет принимать запросы (пример: 127.0.0.1, localhost)
     DEBUG - режим откладки Django, локально ставим True, на прод ставим False

     Следующие переменные ставятся только после создания базы данных
     DB_ENGINE - тип базы данных для Django (пример: django.db.backends.postgresql)
     DB_NAME - имя вашей базы данных, задается при создании
     DB_USER - пользователь базы данных
     DB_PASSWORD - пароль от вашей базы данных, задается при создании
     DB_HOST - адрес сервера базы данных (пример: localhost)
     DB_PORT - порт базы данных, задается при создании
      
     EMAIL_BACKEND - backend Django для отправки почты
     EMAIL_HOST - SMTP-сервер почты (пример: Gmail: smtp.gmail.com)
     EMAIL_PORT - порт SMTP-сервера (пример: 587 — TLS)
     EMAIL_HOST_PASSWORD - пароль для SMTP-аутентификации, задается в вашем гугл аккаунте, далее пункты для gmail
       - заходим на https://myaccount.google.com/ -> безопасность -> двухэтапная аутентификация (ее нужно будет подключить) -> пароли приложений -> вводим название нашего приложения (произвольное) и берем предоставленный пароль
     EMAIL_HOST_USER - почта, с которой идет рассылка
     DEFAULT_FROM_EMAIL - email, который будет указан в поле "From"
      
     ITAD_API_KEY - API-ключ сервиса IsThereAnyDeal (Для получения следуйте сюда -> https://isthereanydeal.com/apps/, необходимо зарегистрироваться самому и зарегистрировать свое приложение)
5. Создаем миграции и суперюзера
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

6. Загружаем данные в бд
  6.1 Сначала игры
  python manage.py sync_games

  6.2 После цены к этим играм
  python manage.py sync_prices

7. Далее запускаем сервер
python manage.py runserver

Теперь вы можете проверить его работу на http://127.0.0.1:8000/
