### Hexlet tests and linter status:
[![Actions Status](https://github.com/DonDetta/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/DonDetta/python-project-52/actions)
[![CI](https://github.com/DonDetta/python-project-52/actions/workflows/ci.yml/badge.svg)](https://github.com/DonDetta/python-project-52/actions/workflows/ci.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=DonDetta_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=DonDetta_python-project-52)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=DonDetta_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=DonDetta_python-project-52)

---

## Менеджер задач

Веб-приложение для управления задачами, построенное на Django. Позволяет командам создавать задачи, назначать исполнителей, отслеживать статусы и группировать задачи по меткам.

### Возможности

- Регистрация и аутентификация пользователей
- Создание, редактирование и удаление задач
- Управление статусами задач (новый, в работе, на тестировании, завершён и др.)
- Метки для гибкой категоризации задач
- Фильтрация задач по статусу, исполнителю, метке и автору
- Просмотр детальной страницы задачи

### Стек

- Python 3.13, Django 6
- PostgreSQL (продакшен) / SQLite (разработка)
- Bootstrap 5
- Gunicorn + Whitenoise
- Деплой на Render.com
- Мониторинг ошибок через Rollbar

### Установка и запуск

```bash
# Установить зависимости
make install

# Применить миграции
make migrate

# Запустить сервер разработки
make dev
```

Скопируй `.env.example` в `.env` и задай переменные окружения перед запуском.

### Demo:
https://python-project-52-1-jebl.onrender.com
