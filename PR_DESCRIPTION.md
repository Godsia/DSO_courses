# PR: P08 - CI/CD Minimal

## Описание

Реализация минимального CI/CD pipeline с автоматическими тестами, линтингом, кэшированием и эмуляцией деплоя.

## Реализованные компоненты

### 1. CI Workflow
- **Файл:** [`.github/workflows/ci.yml`](.github/workflows/ci.yml)
- **События:** push и pull_request
- **Python:** 3.12
- **Таймауты:** 10 минут для тестов, 5 минут для деплоя

### 2. Сборка и тесты (C1)
- ✅ Установка зависимостей через pip
- ✅ Unit-тесты: pytest с покрытием
- ✅ Линтеры: ruff, black --check, isort --check-only
- ✅ CI run зелёный

### 3. Кэширование и конкурренси (C2)
- ✅ **Кэш pip:** `actions/cache@v4` для зависимостей
- ✅ **Ключ кэша:** `${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}`
- ✅ **Concurrency:** настроен для предотвращения дубликатов
- ✅ **Cancel in progress:** отменяет предыдущие запуски

### 4. Секреты и конфиги (C3)
- ✅ **Секреты:** `${{ secrets.STAGING_ENV }}` в deploy шаге
- ✅ **Permissions:** `contents: read` настроены
- ✅ **Маскирование:** секреты автоматически маскируются в логах
- ✅ **Environment:** staging окружение с URL

### 5. Артефакты и отчеты (C4)
- ✅ **Test reports:** `reports/` директория
- ✅ **Coverage:** HTML и XML форматы
- ✅ **JUnit XML:** `reports/junit.xml`
- ✅ **Deployment artifacts:** `artifacts/` для staging
- ✅ **Retention:** 7 дней для тестов, 30 дней для деплоя

### 6. CD/промоушн (эмуляция) (C5)
- ✅ **Staging deploy:** job запускается на push в main
- ✅ **Dry-run:** симуляция деплоя без реального деплоя
- ✅ **Artifacts:** создание deployment артефактов
- ✅ **Environment:** использование GitHub Environments

## Структура проекта

```
.
├── .github/workflows/ci.yml  # CI/CD workflow
├── src/app/                  # Исходный код
├── tests/                    # Тесты
├── reports/                  # Отчёты (генерируются)
├── requirements.txt          # Зависимости
└── pyproject.toml           # Конфигурация инструментов
```

## Workflow Jobs

### 1. Test and Lint
- Установка зависимостей с кэшированием
- Линтинг: ruff, black, isort
- Тестирование: pytest с coverage
- Загрузка артефактов: test reports

### 2. Deploy (Staging)
- Запускается только на push в main
- Симуляция деплоя в staging
- Создание deployment артефактов

## Кэширование

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

## Артефакты

### Test Reports
- `reports/junit.xml` - JUnit XML для CI интеграции
- `reports/coverage.xml` - Coverage в XML формате
- `reports/coverage/` - HTML coverage отчёт

### Deployment Artifacts
- `artifacts/deploy.log` - Лог деплоя
- `artifacts/version.txt` - Версия деплоя

## Секреты

Настроены в GitHub Settings → Secrets and variables → Actions:
- `STAGING_ENV` - переменная для staging окружения (опционально)

## Concurrency

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

Предотвращает параллельные запуски одного и того же workflow.

## Чек-лист

См. [`practices/P08/02_checklist.md`](practices/P08/02_checklist.md)

## Доказательства

### CI Run
- Ссылка на успешный run: [Actions](https://github.com/Godsia/DSO_courses/actions)
- Все проверки проходят: ✅

### Артефакты
- Test reports: доступны в CI run → Artifacts → test-reports
- Deployment artifacts: доступны в CI run → Artifacts → deployment-artifacts

### Секреты
- Настроены в Settings → Secrets and variables → Actions
- Используются через `${{ secrets.STAGING_ENV }}`

## Критерии выполнения

- ✅ **C1:** Сборка и тесты проходят
- ✅ **C2:** Кэширование и concurrency настроены
- ✅ **C3:** Секреты вынесены, permissions настроены
- ✅ **C4:** Артефакты сохраняются
- ✅ **C5:** CD эмуляция (staging deploy) настроена

