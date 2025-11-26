# P09 — Чек-лист сдачи

## C1. SBOM — покрытие и автоматизация (★1)

**Статус:** ✅ Выполнено

**Доказательства:**
- ✅ Workflow автоматически генерирует SBOM при push/workflow_dispatch
- ✅ Используется Syft для генерации SBOM
- ✅ Формат: CycloneDX JSON
- ✅ Результат сохраняется в `EVIDENCE/P09/sbom.json`
- ✅ Доступен через артефакты Actions

**Workflow:** `.github/workflows/ci-sbom-sca.yml`
**Инструмент:** Syft (anchore/sbom-action@v0)
**Формат:** CycloneDX JSON

---

## C2. SCA — отчёт и сводка по уязвимостям (★1)

**Статус:** ✅ Выполнено

**Доказательства:**

### SCA сканирование:
- ✅ Запускается на основе SBOM
- ✅ Используется Grype (anchore/scan-action@v3)
- ✅ Отчёт сохраняется в `EVIDENCE/P09/sca_report.json`

### Сводка:
- ✅ Генерируется `EVIDENCE/P09/sca_summary.md`
- ✅ Содержит агрегированную сводку по severity (Critical/High/Medium/Low)
- ✅ Включает дату генерации и commit SHA

**Workflow:** `.github/workflows/ci-sbom-sca.yml`
**Инструмент:** Grype
**Отчёты:** sca_report.json, sca_summary.md

---

## C3. Артефакты и трассировка (Evidence & DS1) (★1)

**Статус:** ✅ Выполнено

**Доказательства:**

### Артефакты в EVIDENCE/P09/:
- ✅ `sbom.json` - SBOM в формате CycloneDX
- ✅ `sca_report.json` - Полный отчёт SCA
- ✅ `sca_summary.md` - Сводка по уязвимостям

### Загрузка артефактов:
- ✅ Используется `actions/upload-artifact@v4`
- ✅ Имя артефакта: `sbom-sca-evidence`
- ✅ Retention: 30 дней

**Артефакты:** Actions → Run → Artifacts → sbom-sca-evidence

---

## C4. Политика и waivers (★1)

**Статус:** ✅ Выполнено

**Доказательства:**
- ✅ Файл `policy/waivers.yml` создан
- ✅ Содержит базовую структуру полей
- ✅ Пример waiver для демонстрации структуры

**Файл:** `policy/waivers.yml`
**Структура:**
- id, package, vulnerability, severity
- reason, issue, expires, reviewed_by, notes

**Использование:** Планируется использовать для исключений уязвимостей с обоснованием и сроками пересмотра.

---

## C5. Интеграция в CI и гигиена (★1)

**Статус:** ✅ Выполнено

**Доказательства:**

### Триггеры:
- ✅ `workflow_dispatch` - ручной запуск
- ✅ `push` по релевантным путям (requirements*.txt, *.py, workflow)
- ✅ `pull_request` по релевантным путям

### Безопасность:
- ✅ Permissions: `contents: read` (минимальные права)
- ✅ Не использует секреты
- ✅ Работает только с публичными образами

### Оптимизация:
- ✅ Concurrency настроен (предотвращает дубликаты)
- ✅ Таймаут: 15 минут
- ✅ Артефакты загружаются через upload-artifact

**Workflow:** `.github/workflows/ci-sbom-sca.yml`
**Интеграция:** Не конфликтует с ci.yml из P08

---

## Итоговая оценка

- **C1:** ★1 - SBOM автоматически генерируется, сохраняется в EVIDENCE/P09/
- **C2:** ★1 - SCA отчёт и сводка генерируются
- **C3:** ★1 - Все артефакты в EVIDENCE/P09/, доступны через Actions
- **C4:** ★1 - policy/waivers.yml создан с базовой структурой
- **C5:** ★1 - Workflow интегрирован в CI, правильные триггеры и permissions

**Общая оценка:** 5★ (базовый уровень выполнен)

---

## Дополнительные материалы

- **Workflow:** `.github/workflows/ci-sbom-sca.yml`
- **Артефакты:** EVIDENCE/P09/ (sbom.json, sca_report.json, sca_summary.md)
- **Политика:** `policy/waivers.yml`
- **CI logs:** Actions → Security - SBOM & SCA

