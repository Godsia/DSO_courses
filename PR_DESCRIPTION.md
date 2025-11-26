# PR: P08 - CI/CD Minimal

## Описание

Реализация минимального CI/CD pipeline с автоматическими тестами, линтингом, кэшированием и эмуляцией деплоя.

## Реализованные компоненты

### C1. Сборка и тесты
- ✅ Python 3.12, установка зависимостей через pip
- ✅ Линтеры: ruff, black --check, isort --check-only
- ✅ Тесты: pytest с coverage
- ✅ CI run зелёный

### C2. Кэширование и конкурренси
- ✅ Кэш pip через `actions/cache@v4`
- ✅ Ключ: `${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}`
- ✅ Concurrency с `cancel-in-progress: true`

### C3. Секреты и конфиги
- ✅ Секреты: `${{ secrets.STAGING_ENV }}` в deploy шаге
- ✅ Permissions: `contents: read`
- ✅ Автоматическое маскирование секретов

### C4. Артефакты и отчеты
- ✅ Test reports: JUnit XML, coverage (HTML/XML)
- ✅ Deployment artifacts: deploy.log, version.txt
- ✅ Retention: 7 дней для тестов, 30 дней для деплоя

### C5. CD/промоушн (эмуляция)
- ✅ Staging deploy job на push в main
- ✅ Dry-run симуляция деплоя
- ✅ Environment: staging с URL

## Workflow

**Файл:** [`.github/workflows/ci.yml`](.github/workflows/ci.yml)

### Jobs:
1. **Test and Lint** - запускается на push и PR
   - Линтинг (ruff, black, isort)
   - Тесты (pytest с coverage)
   - Загрузка артефактов

2. **Deploy (Staging)** - запускается только на push в main
   - Симуляция деплоя
   - Создание deployment артефактов

## Доказательства

- **CI Run:** [Actions](https://github.com/Godsia/DSO_courses/actions/workflows/ci.yml) ✅
- **Артефакты:** test-reports, deployment-artifacts
- **Секреты:** Settings → Secrets and variables → Actions
- **Чек-лист:** [`practices/P08/02_checklist.md`](practices/P08/02_checklist.md)

## Критерии выполнения

- ✅ **C1:** Сборка и тесты проходят
- ✅ **C2:** Кэширование и concurrency настроены
- ✅ **C3:** Секреты вынесены, permissions настроены
- ✅ **C4:** Артефакты сохраняются
- ✅ **C5:** CD эмуляция (staging deploy) настроена

