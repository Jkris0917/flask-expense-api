# 💴 Expense Tracker REST API

A RESTful API built with Flask and Python.
Designed to manage daily expenses with full CRUD operations
and category-based reporting.

## Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/expenses` | List all expenses |
| POST | `/expenses` | Create new expense |
| GET | `/expenses/<id>` | Get one expense |
| PUT | `/expenses/<id>` | Update expense |
| DELETE | `/expenses/<id>` | Delete expense |
| GET | `/summary` | Totals and category breakdown |

## Tech stack
- Python 3.12
- Flask
- PostgreSQL
- Flask-SQLAlchemy
- python-dotenv

## Setup

```bash
git clone https://github.com/Jkris0917/flask-expense-api
cd flask-expense-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Create a .env file:
# DATABASE_URL=postgresql://postgres:PASSWORD@localhost:5432/expense_tracker

python app.py
```

## What I learned

- REST API design principles (HTTP methods, status codes)
- Separating business logic (models.py) from HTTP layer (app.py)
- Input validation and error handling in API endpoints
- Environment configuration with python-dotenv

---

# 💴 経費管理 REST API

FlaskとPythonで作ったRESTful APIです。
支出の登録・編集・削除・検索と、カテゴリ別集計に対応しています。

## 使い方

```bash
pip install -r requirements.txt
python app.py
```