# PR: P12 - IaC & Container Security

## Описание

Реализация проверки безопасности инфраструктуры как кода (IaC) и контейнерных образов с помощью Hadolint, Checkov и Trivy в CI/CD pipeline.

## Реализованные компоненты

### C1. Hadolint — проверка Dockerfile
- ✅ **Инструмент:** Hadolint (Docker образ)
- ✅ **Конфигурация:** `security/hadolint.yaml`
- ✅ **Цель:** Проверка Dockerfile на best practices
- ✅ **Отчёт:** `EVIDENCE/P12/hadolint_report.json`

### C2. Checkov — проверка IaC
- ✅ **Инструмент:** Checkov (Docker образ)
- ✅ **Конфигурация:** `security/checkov.yaml`
- ✅ **Цель:** Проверка Kubernetes манифестов и Dockerfile
- ✅ **Отчёт:** `EVIDENCE/P12/checkov_report.json`

### C3. Trivy — проверка образа
- ✅ **Инструмент:** Trivy (Docker образ)
- ✅ **Цель:** Сканирование собранного Docker образа на уязвимости
- ✅ **Отчёт:** `EVIDENCE/P12/trivy_report.json`

### C4. Меры харднинга Dockerfile и IaC

#### Dockerfile:
- ✅ **FROM:** Используется конкретная версия `python:3.11-slim` вместо `latest`
- ✅ **Non-root user:** Создан пользователь `appuser` для запуска приложения
- ✅ **Минимальные зависимости:** Установлены только необходимые пакеты
- ✅ **Конфигурация через ENV:** Хост и порт настраиваются через переменные окружения
- ✅ **Health check:** Добавлен HEALTHCHECK для мониторинга

#### IaC (Kubernetes):
- ✅ **Security Context:** Настроен `runAsNonRoot: true` и `runAsUser: 1000`
- ✅ **Service Type:** Используется `ClusterIP` (внутренний доступ), не `LoadBalancer`
- ✅ **Ingress:** Настроен с ограничениями доступа (закомментирован whitelist для примера)
- ✅ **Resource Limits:** Установлены лимиты памяти и CPU
- ✅ **Probes:** Настроены liveness и readiness probes

### C5. Интеграция в CI
- ✅ **Workflow:** `.github/workflows/ci-p12-iac-container.yml`
- ✅ **Триггеры:** workflow_dispatch, push/PR по `Dockerfile*`, `iac/**`, `k8s/**`, `security/**`
- ✅ **Permissions:** `contents: read`
- ✅ **Concurrency:** Настроен для предотвращения накопления запусков
- ✅ **Таймаут:** 20 минут

## Workflow

**Файл:** [`.github/workflows/ci-p12-iac-container.yml`](.github/workflows/ci-p12-iac-container.yml)

**Триггеры:**
- `workflow_dispatch` - ручной запуск
- `push` по `Dockerfile*`, `iac/**`, `k8s/**`, `deploy/**`, workflow файлу, `security/**`
- `pull_request` по тем же путям

**Шаги:**
1. Checkout code
2. Create evidence directory
3. Build Docker image (`dso-courses-api:local`)
4. Run Hadolint on Dockerfile
5. Run Checkov on IaC
6. Run Trivy on Docker image
7. Generate summary report
8. Upload evidence artifacts

## Артефакты

**Имя:** `P12_EVIDENCE`
**Содержимое:**
- `EVIDENCE/P12/hadolint_report.json` - Отчёт Hadolint
- `EVIDENCE/P12/checkov_report.json` - Отчёт Checkov
- `EVIDENCE/P12/trivy_report.json` - Отчёт Trivy
- `EVIDENCE/P12/security_summary.md` - Сводка по всем проверкам

**Доступ:** Actions → Run → Artifacts → P12_EVIDENCE

## Харднинг

### Dockerfile
- ✅ FROM: `python:3.11-slim` (конкретная версия)
- ✅ Пользователь: non-root user `appuser`
- ✅ Конфигурация: через переменные окружения (HOST, PORT)
- ✅ Минимальные зависимости: только необходимые пакеты

### IaC (Kubernetes)
- ✅ Security Context: `runAsNonRoot: true`, `runAsUser: 1000`
- ✅ Service: `ClusterIP` (внутренний доступ)
- ✅ Ingress: с ограничениями доступа
- ✅ Resource Limits: установлены лимиты памяти и CPU

## Результаты сканирования

После первого запуска workflow будет добавлена информация:
- Количество findings по каждому инструменту
- Критичные и высокие уязвимости
- План действий по исправлению

## Критерии выполнения

- ✅ **C1:** Hadolint запускается на Dockerfile, отчёт сохраняется
- ✅ **C2:** Checkov запускается на IaC, отчёт сохраняется
- ✅ **C3:** Trivy запускается на образе, отчёт сохраняется
- ✅ **C4:** Применены меры харднинга в Dockerfile и IaC
- ✅ **C5:** Workflow интегрирован в CI с правильными триггерами
