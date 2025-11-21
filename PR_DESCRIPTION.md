# PR: P07 - Container Hardening

## Описание

Реализация практики контейнеризации приложения с применением практик безопасности и харднинга.

## Реализованные компоненты

### 1. Dockerfile (Multi-stage build)
- **Файл:** [`Dockerfile`](Dockerfile)
- **Особенности:**
  - Multi-stage build для уменьшения размера образа
  - Базовый образ: `python:3.11-slim` (минимальный размер)
  - Non-root пользователь (appuser, UID 1000)
  - HEALTHCHECK настроен (интервал 30s, таймаут 3s)
  - Оптимизированные слои без dev-инструментов в финальном образе

### 2. docker-compose.yml
- **Файл:** [`docker-compose.yml`](docker-compose.yml)
- **Особенности:**
  - Локальный запуск приложения
  - Healthcheck настроен
  - Read-only файловая система
  - `no-new-privileges: true` для безопасности
  - tmpfs для временных файлов

### 3. Безопасность контейнера
- ✅ Запуск под non-root пользователем (проверка: `docker compose exec app id -u` != 0)
- ✅ HEALTHCHECK в Dockerfile и docker-compose.yml
- ✅ Read-only файловая система
- ✅ `no-new-privileges` включен
- ✅ Минимальный базовый образ (slim)

### 4. CI/CD интеграция
- **Файл:** [`.github/workflows/ci.yml`](.github/workflows/ci.yml)
- **Проверки:**
  - **Hadolint** - линтинг Dockerfile на best practices
  - **Trivy** - сканирование образа на уязвимости (CRITICAL, HIGH)
  - Автоматическое тестирование контейнера
  - Проверка non-root пользователя

### 5. Дополнительные файлы
- **Makefile** - удобные команды (`make build`, `make up`, `make test`, `make lint`, `make scan`)
- **scripts/test_container.sh** - скрипт для тестирования контейнера
- **.dockerignore** - исключения для сборки образа

## Оптимизации

### Размер образа
- Multi-stage build удаляет временные зависимости
- Использование slim образа вместо полного
- Минимальные слои в финальном образе

### Безопасность
- Non-root пользователь предотвращает привилегированные атаки
- Read-only FS ограничивает возможность записи
- `no-new-privileges` предотвращает эскалацию привилегий
- HEALTHCHECK для мониторинга состояния

### Базовый образ
Выбран `python:3.11-slim` потому что:
- Минимальный размер (~45MB vs ~300MB для полного образа)
- Содержит только необходимые компоненты
- Регулярно обновляется с патчами безопасности
- Поддерживает все необходимые функции Python

## Тестирование

### Локальный запуск
```bash
# Сборка и запуск
make build
make up

# Проверка
curl http://localhost:8000/
curl http://localhost:8000/api/info
```

### Проверка безопасности
```bash
# Проверка non-root
docker compose exec app id -u

# Проверка healthcheck
docker compose ps

# Линтинг Dockerfile
make lint

# Сканирование на уязвимости
make scan
```

## Отчёты сканеров

### Hadolint
- Интегрирован в CI
- Проверяет Dockerfile на соответствие best practices
- Локально: `make lint` или `docker run --rm -i hadolint/hadolint < Dockerfile`

### Trivy
- Интегрирован в CI
- Сканирует образ на уязвимости
- Формат: SARIF для GitHub Security
- Локально: `make scan`
- Отчёт доступен в артефактах CI после запуска

## Чек-лист

См. [`practices/P07/02_checklist.md`](practices/P07/02_checklist.md)

## Критерии выполнения

- ✅ **C1**: Multi-stage build, оптимизированный размер образа
- ✅ **C2**: Non-root пользователь, HEALTHCHECK, read-only FS, no-new-privileges
- ✅ **C3**: docker-compose.yml работает, приложение поднимается
- ✅ **C4**: Hadolint и Trivy интегрированы в CI
- ✅ **C5**: Приложение контейнеризировано и доступно по HTTP

## Доказательства

### Dockerfile
- Ссылка: [`Dockerfile`](Dockerfile)
- Multi-stage build реализован
- Non-root пользователь настроен
- HEALTHCHECK добавлен

### docker-compose.yml
- Ссылка: [`docker-compose.yml`](docker-compose.yml)
- Сервис настроен и работает
- Security options применены

### Отчёты сканеров
- Hadolint: см. логи CI (шаг "Run Hadolint")
- Trivy: см. логи CI (шаг "Run Trivy vulnerability scanner") и артефакты

### Размер образа
```bash
docker images secure-app
# Покажет размер оптимизированного образа
```

### Проверка non-root
```bash
docker compose exec app id -u
# Должно вернуть 1000 (не 0)
```

### Healthcheck
```bash
docker compose ps
# Должно показать статус "healthy"
```

## Связи с предыдущими практиками

- **P06 (Secure Coding)**: Применены практики безопасного программирования в контейнеризированном приложении

