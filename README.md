[![foodgram-project](https://github.com/IvanProhorov/foodgram-project/actions/workflows/main.yml/badge.svg)](https://github.com/IvanProhorov/foodgram-project/actions/workflows/main.yml)
# foodgram-project — [«Продуктовый помощник»](http://178.154.211.92/)	
Приложение «Продуктовый помощник»: сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.
## Подготовка к работе:

1) Клонируйте репозиторий на локальную машину.  
   ```
   git clone https://github.com/IvanProhorov/foodgram-project.git
   ```
2) Создайте файл .env и заполните его своими значениями. Все нужные переменные и их примерные значения описаны файле .env.template.

3) Запустите процесс сборки и запуска контейнеров:  
   ```
   docker-compose up
   ```
4) Чтобы применить миграции, введите:  
   ```
   docker-compose -f docker-compose.yaml exec web python manage.py migrate --noinput
   ```
5) Для создания суперпользователя, необходимо ввести:  
   ```
   docker-compose -f docker-compose.yaml exec web python manage.py createsuperuser
   ```
6) Чтобы добавить в базу ингредиенты и теги:  
   ```
   docker-compose -f docker-compose.yaml exec web python manage.py load_ingredients_data
   ```
7) Чтобы собрать статические файлы, используйте команду:  
   ```
   docker-compose -f docker-compose.yaml exec web python manage.py collectstatic
   ```
   
## Технологии
* [Python](https://www.python.org/) - высокоуровневый язык программирования общего назначения;
* [Django](https://www.djangoproject.com/) - фреймворк для веб-приложений;
* [Django REST framework](https://www.django-rest-framework.org/) - API фреймворк для Django;
* [PostgreSQL](https://www.postgresql.org/) - объектно-реляционная система управления базами данных;
* [Nginx](https://nginx.org/) - HTTP-сервер и обратный прокси-сервер, почтовый прокси-сервер, а также TCP/UDP прокси-сервер общего назначения;
* [Docker](https://www.docker.com/) - ПО для автоматизации развёртывания и управления приложениями в средах с поддержкой контейнеризации;
* [Docker-Compose](https://docs.docker.com/compose/) - инструмент для создания и запуска многоконтейнерных Docker приложений. 
