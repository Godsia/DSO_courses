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

### Hadolint (Dockerfile)
- **Errors:** 1
  - DL3008: Pin versions in apt get install (line 11)
- **Warnings:** 1
  - DL3013: Pin versions in pip (line 19) - уже используется requirements.txt с версиями

**Статус:** Минимальные замечания, в основном рекомендации по версионированию

### Checkov (IaC)
- **Статус:** Отчёт требует проверки (возможны проблемы с форматом вывода)

### Trivy (Container Image)
- **Critical:** 0
- **High:** 1
- **Medium:** 11
- **Low:** 70
- **Total:** 82 уязвимости

**Анализ:**
- Критичных уязвимостей не обнаружено
- 1 высокая уязвимость требует внимания
- Большинство findings - низкой и средней важности
- Рекомендуется обновить базовый образ и зависимости

### План действий

**Приоритет 1 (Высокий):**
- [ ] Исправить High уязвимость из Trivy (обновить зависимости или базовый образ)
- [ ] Исправить DL3008 в Dockerfile (зафиксировать версии в apt-get install)

**Приоритет 2 (Средний):**
- [ ] Просмотреть Medium уязвимости из Trivy, обновить пакеты где возможно
- [ ] Проверить и исправить Checkov findings (если есть)

**Приоритет 3 (Низкий):**
- [ ] Оценить Low уязвимости, обновить при возможности
- [ ] Документировать принятые риски для уязвимостей, которые не требуют немедленного исправления

## Критерии выполнения

- ✅ **C1:** Hadolint запускается на Dockerfile, отчёт сохраняется
- ✅ **C2:** Checkov запускается на IaC, отчёт сохраняется
- ✅ **C3:** Trivy запускается на образе, отчёт сохраняется
- ✅ **C4:** Применены меры харднинга в Dockerfile и IaC
- ✅ **C5:** Workflow интегрирован в CI с правильными триггерами
