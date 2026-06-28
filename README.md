# Cash Management / ДДС

Веб-приложение для управления движением денежных средств (ДДС).

Проект позволяет создавать, редактировать, удалять и просматривать записи о денежных операциях, а также управлять справочниками: статусами, типами операций, категориями и подкатегориями.

## Возможности

* Создание записей ДДС
* Просмотр списка записей
* Редактирование записей
* Удаление записей
* Фильтрация записей:

  * по периоду дат
  * по статусу
  * по типу операции
  * по категории
  * по подкатегории
* Управление справочниками:

  * статусы
  * типы операций
  * категории
  * подкатегории
* Логические зависимости:

  * категория привязана к типу операции
  * подкатегория привязана к категории
  * при создании записи нельзя выбрать категорию не от выбранного типа
  * при создании записи нельзя выбрать подкатегорию не от выбранной категории

## Стек

* Python 3.12
* Django
* Django ORM
* PostgreSQL
* Docker / Docker Compose
* Bootstrap 5
* pgAdmin 4

## Структура проекта

```text
cash-managment/
├── cashflow/
│   ├── management/commands/
│   │   └── seed_cashflow.py
│   ├── migrations/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── config/
│   ├── settings.py
│   └── urls.py
├── templates/
│   ├── base.html
│   └── cashflow/
│       ├── record_list.html
│       ├── record_form.html
│       ├── record_confirm_delete.html
│       ├── reference_list.html
│       ├── reference_form.html
│       └── reference_confirm_delete.html
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── manage.py
```

## Запуск проекта через Docker

### 1. Клонировать репозиторий

```bash
git clone <repository-url>
cd cash-managment
```

### 2. Создать `.env`

Скопируйте пример переменных окружения:

```bash
cp .env.example .env
```

Для Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Пример содержимого `.env`:

```env
SECRET_KEY=change-me
DEBUG=True

POSTGRES_DB=cashflow_db
POSTGRES_USER=cashflow_user
POSTGRES_PASSWORD=change-me
POSTGRES_HOST=db
POSTGRES_PORT=5432

PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=change-me
```

Файл `.env` не должен попадать в Git.

### 3. Собрать Docker-образ

```bash
docker compose build
```

### 4. Запустить PostgreSQL и pgAdmin

```bash
docker compose up -d db pgadmin
```

`pgAdmin` используется только как удобный интерфейс для просмотра базы данных. Для работы самого приложения он не обязателен, но добавлен в Docker Compose, чтобы проверяющий мог при необходимости посмотреть таблицы и данные через браузер.

### 5. Применить миграции

```bash
docker compose run --rm web python manage.py migrate
```

### 6. Заполнить стартовые справочники

```bash
docker compose run --rm web python manage.py seed_cashflow
```

Команда создаёт базовые данные для проверки приложения:

* статусы:

  * Бизнес
  * Личное
  * Налог
* типы операций:

  * Пополнение
  * Списание
* категории и подкатегории для тестирования зависимостей

Команду можно запускать повторно: дубли не создаются.

### 7. Создать суперпользователя

Этот шаг нужен только для входа в Django Admin.

```bash
docker compose run --rm web python manage.py createsuperuser
```

### 8. Запустить веб-приложение

```bash
docker compose up web
```

После запуска приложение будет доступно по адресу:

```text
http://localhost:8000
```

## Основные страницы

### Главная страница с записями ДДС

```text
http://localhost:8000
```

На странице доступны:

* таблица записей
* фильтры
* создание записи
* редактирование записи
* удаление записи

### Управление справочниками

```text
http://localhost:8000/references/
```

На странице доступны:

* добавление, редактирование и удаление статусов
* добавление, редактирование и удаление типов операций
* добавление, редактирование и удаление категорий
* добавление, редактирование и удаление подкатегорий

Категории связываются с типами операций, а подкатегории — с категориями.

### Django Admin

```text
http://localhost:8000/admin/
```

Админ-панель можно использовать для дополнительной проверки данных.

### pgAdmin

```text
http://localhost:5050
```

Данные для входа берутся из `.env`:

```env
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=change-me
```

Для подключения к PostgreSQL внутри pgAdmin используйте:

```text
Host: db
Port: 5432
Database: cashflow_db
Username: cashflow_user
Password: change-me
```

Важно: `Host` должен быть именно `db`, потому что PostgreSQL запущен внутри Docker Compose-сети.

## Проверка проекта

Проверить настройки Django:

```bash
docker compose run --rm web python manage.py check
```

Применить миграции:

```bash
docker compose run --rm web python manage.py migrate
```

Запустить приложение:

```bash
docker compose up web
```

## Сценарий ручной проверки

1. Открыть главную страницу:

```text
http://localhost:8000
```

2. Перейти в раздел справочников:

```text
http://localhost:8000/references/
```

3. Создать или проверить наличие:

   * статуса
   * типа операции
   * категории
   * подкатегории

4. Вернуться на главную страницу.

5. Создать запись ДДС.

6. Проверить, что:

   * после выбора типа операции доступны только связанные категории
   * после выбора категории доступны только связанные подкатегории
   * сумма обязательна
   * тип, категория и подкатегория обязательны

7. Отредактировать созданную запись.

8. Проверить фильтры на главной странице.

9. Удалить запись.

10. Попробовать удалить справочник, который уже используется в записи. Приложение не должно позволить удалить такой элемент.

## Остановка проекта

Остановить контейнеры:

```bash
docker compose down
```

Остановить контейнеры и удалить данные PostgreSQL:

```bash
docker compose down -v
```

После `docker compose down -v` база будет очищена. Для повторного запуска нужно снова выполнить:

```bash
docker compose up -d db pgadmin
docker compose run --rm web python manage.py migrate
docker compose run --rm web python manage.py seed_cashflow
docker compose up web
```

## Возможные проблемы

### Порт 5432 уже занят

Если локально уже запущен PostgreSQL, порт `5432` может быть занят.

Можно изменить внешний порт в `docker-compose.yml`, например:

```yaml
ports:
  - "5433:5432"
```

При этом внутри Docker Compose значение `POSTGRES_HOST=db` менять не нужно.

### Порт 8000 уже занят

Если порт `8000` занят, измените проброс порта для сервиса `web`:

```yaml
ports:
  - "8001:8000"
```

Тогда приложение будет доступно по адресу:

```text
http://localhost:8001
```

### pgAdmin не открывается

Проверьте, что контейнер запущен:

```bash
docker compose ps
```

Если нужно, перезапустите pgAdmin:

```bash
docker compose up -d pgadmin
```

## Команды для разработки

Создать миграции:

```bash
docker compose run --rm web python manage.py makemigrations
```

Применить миграции:

```bash
docker compose run --rm web python manage.py migrate
```

Заполнить справочники:

```bash
docker compose run --rm web python manage.py seed_cashflow
```

Создать суперпользователя:

```bash
docker compose run --rm web python manage.py createsuperuser
```

Запустить приложение:

```bash
docker compose up web
```

## Примечания по реализации

* Денежная сумма хранится через `DecimalField`, чтобы избежать ошибок округления.
* Для справочников используется `on_delete=PROTECT`, чтобы нельзя было случайно удалить данные, которые уже используются в записях ДДС.
* Проверка зависимостей между типом, категорией и подкатегорией выполняется на стороне сервера.
* Зависимые выпадающие списки категорий и подкатегорий работают через JavaScript и простые JSON endpoints.
* Разграничение прав пользователей не реализовано, так как оно не входило в требования тестового задания.
