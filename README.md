## Установка локально без Docker

1. Установить локально redis(redis-cli.exe) и запустить(redis-server.exe)
   ```bash
   https://github.com/tporadowski/redis
   ```
   Или запустить отдельно в Docker ↓
   
   1.1 Подтянуть образ контейнера
   ```bash
   docker pull redis:7
   ```
   1.2 Запустить контейнер
   ```bash
   docker run --name some-redis -p 6379:6379 -d redis:7
   
3. Склонировать репозиторий:
   ```bash
   git clone https://github.com/Klaxer77/test-python.git
4. Создать виртуальное окружение (от версии python 3.10)
   ```bash
   py -3.11 -m venv venv
5. Активировать виртуальное окружение
   ```bash
   venv\Scripts\activate.ps1
6. Установить зависимости
   ```bash
   pip install -r req.txt
7. Запустить проект от корневой папки
   ```bash
   uvicorn app.main:app --reload
## Установка локально c Docker

1. Склонировать репозиторий:
   ```bash
   git clone https://github.com/Klaxer77/test-python.git
2. Создать образы
   ```bash
   docker-compose -f docker-compose.dev.yml build
3. Запустить проект
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
Документация: 
```bash
http://localhost:8000/docs#/
