# Referral System API

## Описание

**Referral System API** — это API-сервис, реализующий простую реферальную систему.


## Автор
👨‍💻 **Козлов Леонид**  
📧 [GitHub](https://github.com/KozlovL) 


## Технологический стек
### Backend
- Python 3.9
- Django 4.2
- Django REST Framework
- PostgreSQL
- JWT
- Gunicorn

## Локальное развертывание

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/KozlovL/referral_system.git
cd referral_system
```

2. **Настройка виртуального окружения**
```bash
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Создайте .env файл на основе шаблона:**
```bash
cp .env.example .env
```

```bash
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=ваш-secret-key
```

4. **Подготовка базы данных**
```bash
python manage.py migrate
```

5. **Запуск сервера**
```bash
python manage.py runserver
```

Проект доступен по адресу:  
**http://127.0.0.1:8000/**


## Примеры API-запросов

1. **Имитация отправки кода**
```bash
POST /api/send_code/
Content-Type: application/json

{
  "phone": "123456789"
}
```

2. **Авторизация**
```bash
POST /api/verify_code/
Content-Type: application/json

{
  "phone": "123456789",
  "code": "1234"
}
```

Примечание.
Код верификации в проекте статичен и равен "1234".

3. **Профиль**
```bash
GET /api/profile/
Authorization: Bearer <ваш_токен>
```

4. **Использование реферального кода**
```bash
POST /api/use_invite_code/
Authorization: Bearer <ваш_токен>
Content-Type: application/json

{
  "invite_code": "x32bgf"
}
```
