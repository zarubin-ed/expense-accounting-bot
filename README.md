# Телеграм-бот учёта совместных расходов

Телеграм-бот для удобного учёта долгов и совместных расходов между участниками группы. Позволяет регистрировать новые долги, погашать существующие, получать сводную статистику по задолженностям и уведомлять пользователей о том, кто кому должен. Проект реализован на Python 3.10+ с использованием стандартных инструментов разработки.

## Участники проекта 

- Зарубин Егор Б05-427 (@egor_zarubin) - отвественный за взаимодействие с базой данных и бэк. Дополнительная используемая библиотека - peewee.

- Булгаков Денис Б05-417 (@denisbulgakow) - ответственный за бота. Дополнительная используемая библиотека - python-telegram-bot.

## Основной функционал

- Добавление бота в группу: для начала работы необходимо добавить бота в группу Telegram. После этого все члены группы могут взаимодействовать с ботом и вводить свои расходы.

- Регистрация долга: бот позволяет зарегистрировать новый долг, указав имя должника, сумму и, при желании, комментарий (например, повод траты). Долг сохраняется в системе и учитывается в дальнейшем.

- Погашение долга: при оплате долга бот умеет отмечать частичную или полную уплату. Пользователь указывает, какой долг он погашает и на какую сумму, после чего задолженность пересчитывается.

- Вывод статистики: команда статистики показывает текущую сводку по долгам — сколько каждый участник должен другим и сколько ему должны. Это удобная сводная информация для контроля совместных расходов.

- Отметка должников: бот позволяет «тегнуть» участника чата (@username), чтобы уведомить его о его долгах или погашении долга. Это удобно для публичного напоминания в группе.

Примеры команд:
```
/debt add @ivan 100 "Обед в кафе"
/debt repay @ivan 50
/debt stats
```
## Локальный запуск проекта

Чтобы запустить проект локально, выполните следующие шаги:

1. Клонируйте репозиторий. Можно использовать SSH или HTTPS:

```
git clone git@github.com:zarubin-ed/expense-accounting-bot.git

git clone https://github.com/zarubin-ed/expense-accounting-bot.git
```

2. Создайте виртуальное окружение. В корневой директории проекта выполните:

```
python -m venv .venv
```
Активируйте виртуальное окружение:

- На Linux/macOS:
```
source .venv/bin/activate
```
- На Windows:
```
.\.venv\Scripts\activate
```
3. Установите зависимости. В активированном окружении выполните:
```
pip install -r requirements.txt
```
4. Создайте файл .env. В корне проекта создайте файл .env и добавьте в него токен бота:
```
BOT_TOKEN=<ваш_токен_бота>
```
Замените <ваш_токен_бота> на полученный у BotFather токен.

5. Запустите бота. В активированном виртуальном окружении выполните:
```
PYTHONPATH=src python main.py
```
После запуска бот подключится к Telegram и начнёт обрабатывать команды в группах, куда его добавили.

## Запуск тестов

Для запуска тестов и проверки покрытия используйте команду:
```
PYTHONPATH=src python -m pytest --cov src tests --cov-report=term-missing
```
Она запустит тесты из каталога tests и выведет отчёт о покрытии кода.

## Структура проекта

```
.
├── .env
├── README.md
├── requirements.txt
├── src
│   └── main.py
└── tests
    └── test_main.py
```

- .env — файл с конфигурацией (токеном бота).

- README.md — этот файл с описанием проекта.

- requirements.txt — список зависимостей Python.

- src/main.py — исходный код бота.

- tests/ — каталог с тестами (например, test_main.py).

## Минимальные требования

- Python: версия 3.10 или выше.

- Телеграм-бот: должен быть назначен администратором в чате, в котором он будет работать, чтобы иметь права на упоминание пользователей и удаление/редактирование сообщений при необходимости.

- Подключение к Интернету и доступ к Telegram API через токен бота.