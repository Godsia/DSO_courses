# PR: P10 - SAST & Secrets

## Описание

Реализация автоматического статического анализа кода (SAST) с помощью Semgrep и сканирования секретов с помощью Gitleaks в CI/CD pipeline.

## Реализованные компоненты

### C1. SAST — Semgrep с SARIF отчётом
- ✅ **Инструмент:** Semgrep (Docker образ)
- ✅ **Профиль:** `p/ci` (базовые проверки для CI)
- ✅ **Дополнительные правила:** `security/semgrep/rules.yml`
  - Обнаружение хардкодных секретов (пароли, API ключи)
  - Обнаружение небезопасного использования `eval()`
- ✅ **Формат отчёта:** SARIF
- ✅ **Артефакт:** `EVIDENCE/P10/semgrep.sarif`

### C2. Secrets Scanning — Gitleaks
- ✅ **Инструмент:** Gitleaks (Docker образ)
- ✅ **Конфигурация:** `security/.gitleaks.toml`
- ✅ **Сканирование:** Текущая рабочая копия репозитория (без истории коммитов)
- ✅ **Формат отчёта:** JSON
- ✅ **Артефакт:** `EVIDENCE/P10/gitleaks.json`

### C3. Артефакты и трассировка
- ✅ Все артефакты в `EVIDENCE/P10/`
- ✅ Загружаются через `actions/upload-artifact@v4`
- ✅ Retention: 30 дней
- ✅ Имя артефакта: `sast-secrets-evidence`

### C4. Триаж и работа с findings
- ✅ Workflow настроен с `|| true` для предотвращения блокировки разработки
- ✅ Конфигурация Gitleaks включает allowlist для известных false positives
- ✅ Правила Semgrep настроены под проект

### C5. Интеграция в CI
- ✅ Workflow: `.github/workflows/ci-sast-secrets.yml`
- ✅ Триггеры: workflow_dispatch, push/PR по релевантным путям
- ✅ Permissions: `contents: read`
- ✅ Concurrency настроен
- ✅ Таймаут: 15 минут

## Workflow

**Файл:** [`.github/workflows/ci-sast-secrets.yml`](.github/workflows/ci-sast-secrets.yml)

**Триггеры:**
- `workflow_dispatch` - ручной запуск
- `push` по `**/*.py`, `**/*.js`, `**/*.ts`, `**/*.yml`, `**/*.yaml`, workflow файлу, `security/**`
- `pull_request` по тем же путям

**Шаги:**
1. Checkout code
2. Create evidence directory
3. Run Semgrep SAST scan (с профилем `p/ci` и кастомными правилами)
4. Run Gitleaks secrets scan
5. Upload evidence artifacts

## Артефакты

**Имя:** `sast-secrets-evidence`
**Содержимое:**
- `EVIDENCE/P10/semgrep.sarif` - Отчёт Semgrep в формате SARIF
- `EVIDENCE/P10/gitleaks.json` - Отчёт Gitleaks в формате JSON

**Доступ:** Actions → Run → Artifacts → sast-secrets-evidence

## Конфигурация

### Semgrep Rules
**Файл:** [`security/semgrep/rules.yml`](security/semgrep/rules.yml)

Правила для обнаружения:
- Хардкодных секретов (пароли, API ключи)
- Небезопасного использования `eval()`

### Gitleaks Config
**Файл:** [`security/.gitleaks.toml`](security/.gitleaks.toml)

Allowlist для исключения:
- `.git/` директории
- `EVIDENCE/` директории
- Workflow файлы
- Сам конфиг Gitleaks

## Findings и триаж

После первого запуска workflow:
- Проверены отчёты Semgrep и Gitleaks
- False positives добавлены в allowlist `.gitleaks.toml`
- Реальные проблемы зафиксированы для дальнейшей работы

## Критерии выполнения

- ✅ **C1:** Semgrep запускается с профилем `p/ci` и кастомными правилами, SARIF отчёт сохраняется
- ✅ **C2:** Gitleaks запускается с конфигом, JSON отчёт сохраняется
- ✅ **C3:** Артефакты сохраняются в EVIDENCE/P10/
- ✅ **C4:** Триаж findings выполнен, false positives обработаны
- ✅ **C5:** Workflow интегрирован в CI с правильными триггерами и permissions
