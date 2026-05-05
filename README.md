# Дорога Минина: регистрация участников велопробега

Django-приложение для сайта велопробега и регистрации участников. Основной пользовательский сценарий:

1. Участник регистрируется по ФИО, email и телефону.
2. Приложение генерирует пароль и отправляет его выбранным способом: через SMS.ru или на email.
3. Пользователь попадает в профиль.
4. Для активного мероприятия создается заказ (`Order`).
5. Участник выбирает вариант участия, оплачивает через Robokassa.
6. После оплаты выбирает звено (`Place`) и размер футболки (`Merch`).

## Структура проекта

- `dorogaminina_django/` - настройки Django, корневые URL, WSGI/ASGI.
- `home/` - пользователи, регистрация, авторизация, профиль, основные страницы.
- `events/` - мероприятия, заказы, звенья, мерч, партнеры, сообщения и платежные callbacks.
- `blog/` - статьи и категории.
- `templates/` - Django-шаблоны.
- `static/` - исходные CSS/JS/images для локальной разработки и сайта.
- `media/` - пользовательские/админские загруженные файлы, локально не хранить в git.
- `uploads/` - старые/дополнительные загруженные файлы.

## Локальная разработка

Рабочая директория проекта:

```powershell
cd E:\sites\dorogaminina_django
```

Используем существующее виртуальное окружение:

```powershell
..\env_dm\Scripts\Activate.ps1
```

Или запускаем команды без активации:

```powershell
..\env_dm\Scripts\python.exe manage.py check
```

Локальные секреты и ключи хранятся в файле `.config` в корне проекта. Этот файл добавлен в `.gitignore` и не должен попадать в репозиторий.

Для нового окружения можно взять структуру из `.config.example`:

```powershell
Copy-Item .config.example .config
```

После этого заполнить значения в `.config`.

Проверенное окружение:

- Python `3.10.11`
- Django `5.2.1`
- `django-robokassa3==1.4`
- `django-smsru==1.0.4`

Локально проект использует SQLite:

```text
db.sqlite3
```

Окружение определяется автоматически:

- локальный путь проекта -> `DJANGO_ENV=local`, `DEBUG=True`, SQLite;
- путь Jino `/home/users/j/j1228127/...` -> `DJANGO_ENV=production`, `DEBUG=False`, MySQL.

Поведение можно переопределить в `.config`:

```text
DJANGO_ENV=local
DEBUG=True
```

или:

```text
DJANGO_ENV=production
DEBUG=False
```

Если переопределять режим через системные переменные окружения, для `DEBUG` используйте `DJANGO_DEBUG`, а не общую переменную `DEBUG`. На некоторых машинах `DEBUG` уже может быть занята сторонними инструментами.

Запуск dev-сервера:

```powershell
..\env_dm\Scripts\python.exe manage.py runserver
```

Открыть:

```text
http://127.0.0.1:8000/
```

## Статика Локально

В режиме `DEBUG=True` исходная статика берется из:

```text
static/
```

Настройки:

```python
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
```

Если CSS/JS не отображаются, проверить:

```powershell
..\env_dm\Scripts\python.exe manage.py findstatic css/style.css --verbosity 2
```

Ожидаемый результат: Django должен найти файл в `E:\sites\dorogaminina_django\static\css\style.css`.

`STATIC_ROOT` не должен указывать на ту же папку, что и исходная `static/`, иначе `runserver` может не находить CSS через staticfiles finders.

## Тесты

Запуск всех тестов:

```powershell
..\env_dm\Scripts\python.exe manage.py test
```

Сейчас покрыты:

- пересчет свободных мест в `Place`;
- фильтрация `FinalOrderForm` по активному мероприятию, звеньям и мерчу;
- регистрация пользователя с mock SMS;
- логин по телефону и SMS-паролю;
- создание заказа в профиле;
- изменение цены по `delivery=true/false`;
- запрет пересчета цены после оплаты;
- callbacks Robokassa `success` и `paid`.

Предупреждение `ckeditor.W001` при `check` и тестах ожидаемо: установленный `django-ckeditor` использует устаревший CKEditor 4.

## Доставка Пароля

Способ доставки регистрационного пароля задается настройкой:

```python
PASSWORD_DELIVERY_METHOD = "email"
```

Допустимые значения:

- `"email"` - режим по умолчанию: пароль отправляется письмом на email пользователя.
- `"sms"` - пароль отправляется на телефон через SMS.ru.

Настройки темы письма и адреса отправителя:

```python
PASSWORD_DELIVERY_EMAIL_SUBJECT = "Пароль для Дороги Минина"
DEFAULT_FROM_EMAIL = "..."
```

Для режима `"email"` дополнительно нужно настроить стандартные Django email settings в `.config`: `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_SSL`, `EMAIL_USE_TLS` или другие параметры конкретного SMTP.

Для Mail.ru в `EMAIL_HOST_PASSWORD` нужен не обычный пароль от почтового ящика, а пароль приложения. Если указать обычный пароль, SMTP вернет ошибку `Application password is REQUIRED`. Пароль приложения создается в настройках безопасности Mail.ru для внешних приложений.

Для локальной разработки без реальной отправки можно временно поставить:

```text
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Тогда письмо будет выводиться в консоль `runserver`.

Логика доставки находится в `home/password_delivery.py`. Регистрация только создает пользователя, генерирует пароль, сохраняет его в `User.more` и вызывает `send_registration_password(user)`.

## Основные Модели

`home.User`

- кастомная модель пользователя;
- логин по `phone`;
- регистрационный пароль хранится в поле `more` и как Django password hash.

`events.Event`

- мероприятие велопробега;
- приложение ожидает ровно одно активное мероприятие: `Event.objects.get(active=True)`;
- содержит цену, цену дополнительной доставки, тексты страниц, файлы соглашения и изображения.

`events.Order`

- заказ участника на мероприятие;
- создается в профиле через `get_or_create`;
- `active=False` до подтверждения оплаты;
- после оплаты пользователь завершает регистрацию выбором звена и футболки.

`events.Place`

- звено/группа участников;
- поля `amount`, `busy`, `free`;
- `busy/free` пересчитываются при `save()` звена.

`events.Merch`

- футболки/мерч мероприятия;
- в форме показываются только активные варианты текущего мероприятия.

## Основные URL

Все маршруты сейчас описаны в `dorogaminina_django/urls.py`.

- `/` и `/index.html` - главная и регистрация.
- `/login.html` - вход.
- `/logout.html` - выход.
- `/profile.html` - профиль участника и заказ.
- `/prog.html` - программа.
- `/contacts.html` - контакты.
- `/blog.html` - блог.
- `/blog/<slug>/` - статья.
- `/robokassa/success` - успешная оплата.
- `/robokassa/fail` - неуспешная оплата.
- `/robokassa/paid` - callback оплаты.

## Важные Особенности

- Во многих view используется `Event.objects.get(active=True)`. Если активных мероприятий 0 или больше 1, страницы будут падать.
- Robokassa `InvId` формируется как `2000 + order.id`; callbacks вычитают `2000`.
- В профиле цена меняется через query-параметр `delivery=true`, пока заказ не оплачен.
- После оплаты `order.active=True`, цена больше не должна перезаписываться.
- POST выбора звена/футболки должен валидировать форму с `event` и `order`, иначе можно отправить id звена от другого мероприятия.

## Хостинг Jino

Проект развернут на Jino.

```text
SSH host: j1228127.myjino.ru
User: j1228127
Project path: /home/users/j/j1228127/domains/xn--80aahdwa0ajbdax.xn--p1ai
```

Секреты, пароли, API-ключи и доступы не хранить в документации и не коммитить.

Полезные read-only команды:

```bash
cd /home/users/j/j1228127/domains/xn--80aahdwa0ajbdax.xn--p1ai
venv311/bin/python3 manage.py check
venv311/bin/python3 manage.py showmigrations events blog home
git status --short
```

На сервере фактически используется MySQL. Локально используется SQLite.

Настройки окружения на Jino должны быть в серверном `.config`, который не хранится в git. Минимально важные параметры:

```text
DJANGO_ENV=production
DEBUG=False
MYSQL_NAME=...
MYSQL_USER=...
MYSQL_PASSWORD=...
MYSQL_HOST=localhost
MYSQL_PORT=3306
ALLOWED_HOSTS=xn--80aahdwa0ajbdax.xn--p1ai,81.177.165.238
CSRF_TRUSTED_ORIGINS=https://xn--80aahdwa0ajbdax.xn--p1ai,http://xn--80aahdwa0ajbdax.xn--p1ai
```

На момент последней проверки на сервере:

- `venv311/bin/python3` - рабочее окружение с Django;
- `passenger_wsgi.py` перезапускает приложение через `venv311/bin/python3`;
- `.htaccess` указывает на `.venv/python311/bin/python3`, где Django может быть не установлен, поэтому конфигурация окружений требует осторожности;
- `public_html/` содержит собранную статику и media;
- `debug.log` большой и не должен попадать в git.

## Отличия Локально И На Сервере

Перед деплоем обязательно проверять:

```powershell
git status --short
```

На сервере:

```bash
git status --short
git rev-parse HEAD
```

Важно: история миграций `events` локально и на сервере может отличаться.

Локально:

```text
events.0002_event_position_1_event_position_2_alter_event_about_and_more
```

На сервере встречалась:

```text
events.0002_event_position_1_event_position_2
```

Если просто заменить миграции и выполнить `migrate`, Django может попытаться применить уже существующие поля повторно. Перед деплоем такие расхождения нужно выравнивать отдельно.

Текущее правило проекта: папки `migrations` намеренно не хранятся в git. Это временно снижает риск сломать сервер из-за расхождения локальной и серверной истории миграций.

Пока история миграций не выровнена:

- не добавлять миграции через `git add -f` без отдельной проверки сервера;
- не удалять правило `migrations` из `.gitignore`;
- изменения моделей сопровождать отдельным планом миграции для локальной базы и для Jino.

## Деплой Через Git

Рекомендуемый порядок для переноса изменений на Jino:

1. Локально убедиться, что рабочее дерево содержит только нужные изменения:

```powershell
git status --short
..\env_dm\Scripts\python.exe manage.py check
..\env_dm\Scripts\python.exe manage.py test
```

Если менялись модели, отдельно выполнить диагностическую проверку:

```powershell
..\env_dm\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Если команда показывает, что нужны новые миграции, не деплоить это как обычный кодовый релиз. Сначала подготовить отдельный план миграции с учетом серверной базы.

2. Закоммитить изменения и отправить в remote:

```powershell
git add .
git commit -m "..."
git push
```

3. На сервере перед `pull` проверить, нет ли незакоммиченных серверных правок:

```bash
cd /home/users/j/j1228127/domains/xn--80aahdwa0ajbdax.xn--p1ai
git status --short
```

4. Если серверное дерево чистое или правки сохранены отдельно, подтянуть код:

```bash
git pull
venv311/bin/python3 manage.py check
```

`migrate` на сервере выполнять только если заранее понятно, какие миграции будут применены, и они согласованы с текущей серверной историей.

5. Если менялась статика, выполнить сборку:

```bash
venv311/bin/python3 manage.py collectstatic --noinput
```

6. Перезапустить Passenger:

```bash
touch tmp/restart.txt
```

Перед возвращением миграций в git нужно отдельно выровнять расхождение `events.0002`, описанное выше.

## Перед Изменениями

Рекомендуемый порядок:

1. Посмотреть `git status --short`.
2. Запустить `manage.py check`.
3. Запустить тесты.
4. Внести изменение.
5. Снова запустить тесты.
6. Проверить diff.

Команды:

```powershell
git status --short
..\env_dm\Scripts\python.exe manage.py check
..\env_dm\Scripts\python.exe manage.py test
git diff --stat
```
