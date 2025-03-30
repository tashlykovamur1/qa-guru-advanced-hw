## Проект содержит копию сервиса Reqres, написанную на **FastAPI** и **Python**, и api тесты на сервис

### Используемые технологии и инструменты
* **FastAPI** — фреймворк для создания API. 
* **Uvicorn** — ASGI-сервер для запуска FastAPI. 
* **Pytest** — фреймворк для написания и запуска тестов. 
* **Requests** — библиотека для выполнения HTTP-запросов.
* **Pydantic** - библиотека для валидации схем


### Предварительные требования

- Убедитесь, что у вас установлен Python версии 3.12 или выше.
```bash
python --version
```
Установка для macOS (используя Homebrew)
```bash
brew install python@3.12
```
- Установите **uv** для управления зависимостями и виртуальными окружениями.
```bash
pip install uv
uv --version # проверка, что корректно установлен
```

### Установка зависимостей

1. Клонируйте репозиторий:

```bash
  git clone https://github.com/tashlykovamur1/qa-guru-advanced-hw.git
```
2. Создайте и активируйте виртуальное окружение
```commandline
uv venv .venv
source .venv/bin/activate
```
3. Установите зависимости с помощью uv:
```bash
uv pip install -r requirements.txt
```
4. Создайте .env файл с переменными окружения по шаблону .env.sample

### Локальный запуск сервиса

```bash
uvicorn app:app --reload
```
или
```
python app.py
```
Сервис будет доступен по адресу: http://localhost:8002

### Запуск тестов
```bash
# запустить все тесты
pytest 

# запустить смок
pytest -m smoke

# запустить тесты на пагинацию
pytest -m pagination
```

### Структура проекта
* app.py — основной файл приложения FastAPI
* models/ - директория с Pydantic моделями
* tests/ — директория с тестами
* requirements.txt — файл c зависимостями проекта
* pytest.ini - файл с настройками конфигурации pytest
