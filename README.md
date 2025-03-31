# Ihaveplan ⌚

## Установка

1. Создать виртуальное окружение
```bash
python -m venv venv
```

2. Активировать виртуальное окружение
```bash
# Windows
venv\Scripts\activate
# Linux или MacOS
source venv/bin/activate
```

3. Установить зависимости
```bash
find . -name "requirements.txt" -exec pip install -r {} \;
```

4. Установить базу данных
```bash
docker compose up -d
```

5. Запустить проект
```bash
cd app
python main.py
```