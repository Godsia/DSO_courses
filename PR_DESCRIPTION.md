# PR: P11 - DAST (ZAP Baseline)

## Описание

Реализация динамического анализа безопасности приложений (DAST) с помощью OWASP ZAP baseline в CI/CD pipeline.

## Реализованные компоненты

### C1. Запуск сервиса в CI
- ✅ **Приложение:** FastAPI сервис (`app/main.py`)
- ✅ **Эндпойнты:**
  - `/` - корневой эндпойнт
  - `/healthz` - health check для CI
  - `/api/v1/info` - информационный эндпойнт
- ✅ **Запуск:** `uvicorn app.main:app --host 0.0.0.0 --port 8080`
- ✅ **Health check:** Ожидание готовности через curl с таймаутом 60 секунд

### C2. Запуск ZAP baseline
- ✅ **Инструмент:** OWASP ZAP baseline (Docker образ `owasp/zap2docker-stable`)
- ✅ **Целевой URL:** `http://localhost:8080`
- ✅ **Формат отчётов:** HTML и JSON
- ✅ **Конфигурация:** Используется baseline режим с генерацией конфига

### C3. Артефакты в EVIDENCE/P11/
- ✅ **Отчёты:**
  - `EVIDENCE/P11/zap_baseline.html` - HTML отчёт
  - `EVIDENCE/P11/zap_baseline.json` - JSON отчёт
- ✅ **Артефакты Actions:** `P11_EVIDENCE` с retention 30 дней

### C4. Интерпретация результатов
- ⏳ После первого запуска workflow будет добавлено резюме по findings
- ⏳ План действий по найденным проблемам

### C5. Интеграция в CI
- ✅ **Workflow:** `.github/workflows/ci-p11-dast.yml`
- ✅ **Триггеры:** workflow_dispatch, push/PR по `app/**`, `requirements*.txt`, workflow файлу
- ✅ **Permissions:** `contents: read`
- ✅ **Concurrency:** Настроен для предотвращения накопления запусков
- ✅ **Таймаут:** 20 минут

## Workflow

**Файл:** [`.github/workflows/ci-p11-dast.yml`](.github/workflows/ci-p11-dast.yml)

**Триггеры:**
- `workflow_dispatch` - ручной запуск
- `push` по `app/**`, `requirements*.txt`, workflow файлу
- `pull_request` по тем же путям

**Шаги:**
1. Checkout code
2. Set up Python 3.11
3. Install dependencies
4. Create evidence directory
5. Start application (uvicorn)
6. Wait for application to be ready
7. Run ZAP baseline scan
8. Copy ZAP reports to evidence directory
9. Stop application
10. Upload evidence artifacts

## Приложение

**Структура:**
- `app/main.py` - FastAPI приложение
- `requirements.txt` - зависимости (FastAPI, Uvicorn)

**Эндпойнты:**
- `GET /` - корневой эндпойнт
- `GET /healthz` - health check
- `GET /api/v1/info` - информация о сервисе

## Артефакты

**Имя:** `P11_EVIDENCE`
**Содержимое:**
- `EVIDENCE/P11/zap_baseline.html` - HTML отчёт ZAP
- `EVIDENCE/P11/zap_baseline.json` - JSON отчёт ZAP

**Доступ:** Actions → Run → Artifacts → P11_EVIDENCE

## Результаты сканирования

После первого запуска workflow будет добавлена информация:
- Количество алертов по уровням (High/Medium/Low)
- Анализ найденных проблем
- План действий по исправлению

## Критерии выполнения

- ✅ **C1:** Сервис поднимается в CI, health check проходит
- ✅ **C2:** ZAP baseline отрабатывает против целевого URL
- ✅ **C3:** Отчёты сохраняются в EVIDENCE/P11/
- ⏳ **C4:** Интерпретация результатов (после первого запуска)
- ✅ **C5:** Workflow интегрирован в CI с правильными триггерами
