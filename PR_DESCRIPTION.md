# PR: P09 - SBOM & SCA

## Описание

Реализация автоматической генерации SBOM и сканирования уязвимостей зависимостей (SCA) в CI/CD pipeline.

## Реализованные компоненты

### C1. SBOM — покрытие и автоматизация
- ✅ **Инструмент:** Syft (Docker образ)
- ✅ **Формат:** CycloneDX JSON
- ✅ **Автоматизация:** Генерируется при push/workflow_dispatch
- ✅ **Артефакт:** `EVIDENCE/P09/sbom.json`

### C2. SCA — отчёт и сводка по уязвимостям
- ✅ **Инструмент:** Grype (Docker образ)
- ✅ **Вход:** SBOM файл (`EVIDENCE/P09/sbom.json`)
- ✅ **Отчёты:**
  - `EVIDENCE/P09/sca_report.json` - полный отчёт
  - `EVIDENCE/P09/sca_summary.md` - сводка по severity

### C3. Артефакты и трассировка
- ✅ Все артефакты в `EVIDENCE/P09/`
- ✅ Загружаются через `actions/upload-artifact@v4`
- ✅ Retention: 30 дней
- ✅ Имя артефакта: `sbom-sca-evidence`

### C4. Политика и waivers
- ✅ Файл `policy/waivers.yml` создан
- ✅ Базовая структура полей
- ✅ Пример waiver для демонстрации

### C5. Интеграция в CI
- ✅ Workflow: `.github/workflows/ci-sbom-sca.yml`
- ✅ Триггеры: workflow_dispatch, push/PR по релевантным путям
- ✅ Permissions: `contents: read`
- ✅ Concurrency настроен
- ✅ Таймаут: 15 минут

## Workflow

**Файл:** [`.github/workflows/ci-sbom-sca.yml`](.github/workflows/ci-sbom-sca.yml)

**Триггеры:**
- `workflow_dispatch` - ручной запуск
- `push` по `requirements*.txt`, `*.py`, workflow файлу
- `pull_request` по тем же путям

**Шаги:**
1. Checkout code
2. Create evidence directory
3. Generate SBOM with Syft
4. Run SCA scan with Grype
5. Generate SCA summary
6. Upload evidence artifacts

## Артефакты

**Имя:** `sbom-sca-evidence`
**Содержимое:**
- `EVIDENCE/P09/sbom.json` - SBOM в формате CycloneDX
- `EVIDENCE/P09/sca_report.json` - Полный отчёт SCA
- `EVIDENCE/P09/sca_summary.md` - Сводка по уязвимостям

**Доступ:** Actions → Run → Artifacts → sbom-sca-evidence

## Политика

**Файл:** [`policy/waivers.yml`](policy/waivers.yml)

Структура для исключений уязвимостей:
- id, package, vulnerability, severity
- reason, issue, expires, reviewed_by, notes

## Доказательства

- **CI Run:** [Actions](https://github.com/Godsia/DSO_courses/actions/workflows/ci-sbom-sca.yml)
- **Артефакты:** EVIDENCE/P09/ (доступны через Actions)
- **Чек-лист:** [`practices/P09/02_checklist.md`](practices/P09/02_checklist.md)

## Критерии выполнения

- ✅ **C1:** SBOM автоматически генерируется
- ✅ **C2:** SCA отчёт и сводка генерируются
- ✅ **C3:** Артефакты сохраняются в EVIDENCE/P09/
- ✅ **C4:** policy/waivers.yml создан
- ✅ **C5:** Workflow интегрирован в CI
