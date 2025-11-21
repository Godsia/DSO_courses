# P07 — Чек-лист сдачи

## C1. Dockerfile (multi-stage, размер) (★1)

**Статус:** ✅ Выполнено

**Доказательства:**
- ✅ Multi-stage build реализован (builder + runtime)
- ✅ Используется python:3.11-slim (минимальный образ)
- ✅ Временные зависимости удалены из финального образа
- ✅ Размер образа оптимизирован

**Dockerfile:** `Dockerfile`
**Размер образа:** Проверить через `docker images secure-app`

---

## C2. Безопасность контейнера (★1)

**Статус:** ✅ Выполнено

**Доказательства:**

### Non-root пользователь:
- ✅ Создан пользователь `appuser` с UID 1000
- ✅ Контейнер запускается под non-root: `USER appuser`
- ✅ Проверка: `docker compose exec app id -u` != 0

### HEALTHCHECK:
- ✅ Настроен в Dockerfile
- ✅ Интервал: 30s, таймаут: 3s, retries: 3
- ✅ Проверка: `docker compose ps` показывает "healthy"

### Read-only файловая система:
- ✅ `read_only: true` в docker-compose.yml
- ✅ `tmpfs` для /tmp и /var/tmp

### Дополнительные меры:
- ✅ `no-new-privileges: true` в docker-compose.yml
- ✅ Минимальный базовый образ (slim)

**Dockerfile:** См. `Dockerfile`
**docker-compose.yml:** См. `docker-compose.yml`

---

## C3. Compose/локальный запуск (★1)

**Статус:** ✅ Выполнено

**Доказательства:**
- ✅ `docker-compose.yml` создан
- ✅ Сервис поднимается: `docker compose up -d`
- ✅ Приложение доступно: `curl http://localhost:8000/`
- ✅ Healthcheck работает

**Файл:** `docker-compose.yml`
**Команды:**
```bash
docker compose up -d
curl http://localhost:8000/
```

---

## C4. Сканирование образа (Trivy/Hadolint) (★1)

**Статус:** ✅ Выполнено

**Доказательства:**

### Hadolint:
- ✅ Интегрирован в CI (`.github/workflows/ci.yml`)
- ✅ Проверяет Dockerfile на best practices
- ✅ Локально: `make lint` или `docker run --rm -i hadolint/hadolint < Dockerfile`

### Trivy:
- ✅ Интегрирован в CI
- ✅ Сканирует образ на уязвимости
- ✅ Формат: SARIF для GitHub Security
- ✅ Локально: `make scan`

**CI конфигурация:** `.github/workflows/ci.yml`
**Отчёты:** В артефактах CI после запуска

---

## C5. Контейнеризация своего приложения (★1)

**Статус:** ✅ Выполнено

**Доказательства:**
- ✅ Flask приложение контейнеризировано
- ✅ Доступно по HTTP: `http://localhost:8000/`
- ✅ Endpoints: `/` (health), `/api/info` (info)
- ✅ Интеграция с CI/CD настроена

**Приложение:** `src/app/main.py`
**Запуск:** `docker compose up -d`
**Проверка:** `curl http://localhost:8000/api/info`

---

## Итоговая оценка

- **C1:** ★1 - Multi-stage build, оптимизированный размер
- **C2:** ★1 - Non-root, healthcheck, read-only, no-new-privileges
- **C3:** ★1 - docker-compose.yml работает
- **C4:** ★1 - Hadolint и Trivy в CI
- **C5:** ★1 - Приложение контейнеризировано и работает

**Общая оценка:** 5★ (базовый уровень выполнен)

---

## Дополнительные материалы

- **Dockerfile** - multi-stage build с безопасностью
- **docker-compose.yml** - конфигурация для локального запуска
- **Makefile** - удобные команды для работы
- **scripts/test_container.sh** - скрипт тестирования
- **CI logs** - логи выполнения CI pipeline с hadolint и trivy

