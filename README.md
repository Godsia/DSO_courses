# P07 - Container Hardening

Контейнеризация приложения с применением практик безопасности.

## Структура

```
.
├── Dockerfile              # Multi-stage build с безопасностью
├── docker-compose.yml      # Локальный запуск
├── .dockerignore          # Исключения для сборки
├── Makefile               # Удобные команды
├── scripts/
│   └── test_container.sh  # Скрипт тестирования
└── src/
    └── app/
        └── main.py        # Flask приложение
```

## Быстрый старт

```bash
# Сборка и запуск
make build
make up

# Или через docker compose
docker compose up -d

# Проверка
curl http://localhost:8000/
curl http://localhost:8000/api/info
```

## Безопасность

- ✅ Multi-stage build для уменьшения размера
- ✅ Запуск под non-root пользователем (UID 1000)
- ✅ Read-only файловая система
- ✅ HEALTHCHECK настроен
- ✅ no-new-privileges включен
- ✅ Минимальный базовый образ (python:3.11-slim)

## Тестирование

```bash
# Локальные тесты
make test

# Или через скрипт
./scripts/test_container.sh

# Линтинг Dockerfile
make lint

# Сканирование на уязвимости
make scan
```

## CI/CD

GitHub Actions автоматически:
- Проверяет Dockerfile через Hadolint
- Сканирует образ на уязвимости через Trivy
- Тестирует запуск контейнера
- Проверяет, что контейнер не запущен под root
